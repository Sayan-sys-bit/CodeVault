from django.contrib import admin
from django.urls import path
from.import views

urlpatterns = [
    path('', views.home, name='home'),
    path('Contact us', views.contact, name='contact'),
    path('About', views.about, name='about'),
    path('search', views.search, name='search')

]
