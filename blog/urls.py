
from django.urls import path
from . import views

urlpatterns = [
    path('', views.blog, name='blog'),
    path('search/', views.search, name='search'),

    path(
        'upload-resource/',
        views.upload_resource,
        name='upload_resource',
    ),
    path(
        'community-resources/',
        views.community_resources,
        name='community_resources',
    ),
    path(
        'my-resources/',
        views.my_resources,
        name='my_resources',
    ),
    path(
        'community-resources/<int:pk>/download/',
        views.download_resource,
        name='resource_download',
    ),

    path(
        'temporary-import/',
        views.temporary_import_page,
        name='temporary_import_page',
    ),
    path(
        'temporary-import-posts/',
        views.temporary_import_posts,
        name='temporary_import_posts',
    ),

    path('<str:slug>/', views.blogpost, name='blogpost'),
]
