from django.urls import path
from . import views

urlpatterns = [
    path('', views.blog, name='blog'),
    path('search/', views.search, name='search'),
    path('<str:slug>/', views.blogpost, name='blogpost'),
]