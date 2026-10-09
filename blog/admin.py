
from django.contrib import admin
from .models import Post, CommunityResource


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'timeStamp')
    search_fields = ('title', 'author')
    prepopulated_fields = {'slug': ('title',)}


@admin.register(CommunityResource)
class CommunityResourceAdmin(admin.ModelAdmin):
    list_display = ('title', 'uploaded_by', 'uploaded_at', 'is_approved')
    list_filter = ('is_approved', 'uploaded_at')
    search_fields = ('title', 'description', 'uploaded_by__username')
    list_editable = ('is_approved',)
    readonly_fields = ('uploaded_at',)