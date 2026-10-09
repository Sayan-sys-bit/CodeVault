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
            uploaded_by=request.user
        )

        return render(request, 'blog/upload_resource.html', {
            'success': 'Your resource has been submitted for admin approval.'
        })

    return render(request, 'blog/upload_resource.html')