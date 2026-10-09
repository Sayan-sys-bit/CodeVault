from django.urls import path
from . import views

urlpatterns = [
    path('', views.blog, name='blog'),
    path('search/', views.search, name='search'),
    path('upload-resource/', views.upload_resource, name='upload_resource'),
    path('<str:slug>/', views.blogpost, name='blogpost'),
]