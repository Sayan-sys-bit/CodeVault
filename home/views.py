from django.shortcuts import render
from home.models import Contact
from django.contrib import messages

def home(request):
    return render(request, 'home/home.html')


def contact(request):
    messages.success(request, 'Welcome to contact us page')
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        content = request.POST.get('content')
        if len(name)<2 or len(email)<3 or len(phone)<10 or len(content)<4:
            messages.error(request, "Please fill the form correctly")
        else:
            contact = Contact(
            name=name,
            email=email,
            phone=phone,
            content=content
        )
        contact.save()

        print("Name:", name)
        print("Email:", email)
        print("Phone:", phone)
        print("Content:", content)

    return render(request, 'home/contact.html')


def about(request):
    return render(request, 'home/about.html')