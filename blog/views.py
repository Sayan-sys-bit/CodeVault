import json
from django.contrib.admin.views.decorators import staff_member_required
from django.views.decorators.http import require_POST
from django.db import transaction, connection
from django.utils.dateparse import parse_datetime
from django.http import JsonResponse
from django.http import FileResponse, Http404, HttpResponseNotFound


from django.shortcuts import render, get_object_or_404, redirect
from .models import Post, CommunityResource
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.contrib.auth.decorators import login_required
import os

def home(request):
    return render(request, 'home/home.html')


@login_required(login_url='login')
def blog(request):
    posts = Post.objects.all().order_by('-timeStamp')
    return render(request, 'blog/bloghome.html', {'posts': posts})


@login_required(login_url='login')
def blogpost(request, slug):
    post = get_object_or_404(Post, slug=slug)
    return render(request, 'blog/blogpost.html', {'post': post})

def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        content = request.POST.get('content')

        contact.objects.create(
            name=name,
            email=email,
            phone=phone,
            content=content
        )

        messages.success(request, 'Your message has been submitted successfully.')

    return render(request, 'home/contact.html')


def about(request):
    return render(request, 'home/about.html')


 



@login_required(login_url='login')
def search(request):
    print("SEARCH VIEW CALLED")
    query = request.GET.get('query', '').strip()
    
    query = request.GET.get('query', '').strip()

    posts = Post.objects.all().order_by('-timeStamp')

    if query:
        posts = posts.filter(title__icontains=query)

    return render(request, 'blog/bloghome.html', {
        'posts': posts,
        'query': query
    })

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            request.session.save()
            return redirect('blog')
        else:
            return render(request, 'home/login.html', {
                'error': 'Invalid username or password.'
            })

    return render(request, 'home/login.html')

    return render(request, 'home/login.html')


def signup_view(request):
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '')
        confirm_password = request.POST.get('confirm_password', '')

        if not username or not email or not password:
            return render(request, 'home/signup.html', {
                'error': 'Please fill in all fields.'
            })

        if password != confirm_password:
            return render(request, 'home/signup.html', {
                'error': 'Passwords do not match.'
            })

        if User.objects.filter(username=username).exists():
            return render(request, 'home/signup.html', {
                'error': 'This username is already taken.'
            })

        if User.objects.filter(email=email).exists():
            return render(request, 'home/signup.html', {
                'error': 'This email is already registered.'
            })

        try:
            validate_password(password)
        except ValidationError as e:
            return render(request, 'home/signup.html', {
                'error': ' '.join(e.messages)
            })

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        login(request, user)
        return redirect('blog')

    return render(request, 'home/signup.html')




@login_required(login_url='login')
def upload_resource(request):
    if request.method == 'POST':
        title = request.POST.get('title', '').strip()
        description = request.POST.get('description', '').strip()
        uploaded_file = request.FILES.get('file')

        if not title or not description or not uploaded_file:
            return render(request, 'blog/upload_resource.html', {
                'error': 'Please fill in all fields and select a file.'
            })

        allowed_extensions = {'.pdf', '.txt', '.docx', '.pptx'}
        extension = os.path.splitext(uploaded_file.name)[1].lower()

        if extension not in allowed_extensions:
            return render(request, 'blog/upload_resource.html', {
                'error': 'Only PDF, TXT, DOCX, and PPTX files are allowed.'
            })

        if uploaded_file.size > 5 * 1024 * 1024:
            return render(request, 'blog/upload_resource.html', {
                'error': 'File size must not exceed 5 MB.'
            })

        CommunityResource.objects.create(
            title=title,
            description=description,
            file=uploaded_file,
            uploaded_by=request.user,
            status=CommunityResource.Status.PENDING,
        )

        messages.success(
            request,
            'Your material has been submitted for admin approval.'
        )

        return redirect('my_resources')

    return render(request, 'blog/upload_resource.html')


def community_resources(request):
    resources = CommunityResource.objects.filter(
        status=CommunityResource.Status.APPROVED
    ).select_related('uploaded_by').order_by('-uploaded_at')

    return render(
        request,
        'blog/community_resources.html',
        {'resources': resources},
    )


@login_required(login_url='login')
def my_resources(request):
    resources = CommunityResource.objects.filter(
        uploaded_by=request.user
    ).order_by('-uploaded_at')

    return render(
        request,
        'blog/my_resources.html',
        {'resources': resources},
    )


def download_resource(request, pk):
    resource = get_object_or_404(CommunityResource, pk=pk)

    is_owner = (
        request.user.is_authenticated
        and resource.uploaded_by_id == request.user.id
    )
    is_staff = (
        request.user.is_authenticated
        and request.user.is_staff
    )

    if (
        resource.status != CommunityResource.Status.APPROVED
        and not (is_owner or is_staff)
    ):
        raise Http404

    if not resource.file:
        raise Http404

    try:
        file_handle = resource.file.open('rb')
    except (FileNotFoundError, OSError, ValueError):
        raise Http404

    filename = os.path.basename(resource.file.name)

    return FileResponse(
        file_handle,
        as_attachment=True,
        filename=filename,
    )


def block_direct_community_media(request, filename):
    return HttpResponseNotFound(
        'Access this material through CodeVault.'
    )


@staff_member_required
@require_POST
def temporary_import_posts(request):
    uploaded_file = request.FILES.get('file')

    if not uploaded_file:
        return JsonResponse(
            {'error': 'Please select posts.json.'},
            status=400
        )

    if uploaded_file.size > 2 * 1024 * 1024:
        return JsonResponse(
            {'error': 'File must be under 2 MB.'},
            status=400
        )

    try:
        data = json.load(uploaded_file)
    except (json.JSONDecodeError, UnicodeDecodeError):
        return JsonResponse(
            {'error': 'Invalid JSON file.'},
            status=400
        )

    if not isinstance(data, list):
        return JsonResponse(
            {'error': 'Unexpected JSON format.'},
            status=400
        )

    records = [
        item for item in data
        if isinstance(item, dict)
        and item.get('model', '').lower() == 'blog.post'
    ]

    if not records:
        return JsonResponse(
            {'error': 'No blog.post records found.'},
            status=400
        )

    created = 0
    skipped = 0

    try:
        with transaction.atomic():
            for record in records:
                fields = record.get('fields', {})
                post_id = record.get('pk')

                required = ('title', 'slug', 'author', 'content')
                if not post_id or not all(
                    key in fields for key in required
                ):
                    return JsonResponse(
                        {'error': 'A record is missing required fields.'},
                        status=400
                    )

                if Post.objects.filter(pk=post_id).exists():
                    skipped += 1
                    continue

                if Post.objects.filter(slug=fields['slug']).exists():
                    skipped += 1
                    continue

                post = Post(
                    sno=post_id,
                    title=fields['title'],
                    slug=fields['slug'],
                    author=fields['author'],
                    content=fields['content'],
                )

                timestamp = fields.get('timeStamp')
                parsed = parse_datetime(timestamp) if timestamp else None

                # bulk_create avoids auto_now_add overwriting timestamps.
                post.save(force_insert=True)

                if parsed:
                    Post.objects.filter(pk=post_id).update(timeStamp=parsed)

                created += 1

            # Synchronize the PostgreSQL primary-key sequence.
            if connection.vendor == 'postgresql':
                table = Post._meta.db_table
                pk_column = Post._meta.pk.column
                with connection.cursor() as cursor:
                    cursor.execute(
                        "SELECT setval(pg_get_serial_sequence(%s, %s), "
                        "COALESCE((SELECT MAX(sno) FROM "
                        + connection.ops.quote_name(table)
                        + "), 1), "
                        "EXISTS (SELECT 1 FROM "
                        + connection.ops.quote_name(table)
                        + "))",
                        [table, pk_column]
                    )

    except Exception:
        return JsonResponse(
            {'error': 'Import failed. Check the Render deployment logs.'},
            status=500
        )

    return JsonResponse({
        'created': created,
        'skipped': skipped,
        'message': 'Import finished.'
    })

@login_required(login_url='login')
def temporary_import_page(request):
    if not request.user.is_staff:
        return HttpResponse(
            'Forbidden: staff access required.',
            status=403
        )

    return render(request, 'temporary_import.html')
