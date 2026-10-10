
from django.contrib import admin
from .models import Post, CommunityResource


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'timeStamp')
    search_fields = ('title', 'author')
    prepopulated_fields = {'slug': ('title',)}



@admin.register(CommunityResource)
class CommunityResourceAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'uploaded_by',
        'uploaded_at',
        'status',
        'review_file_link',
    )

    list_filter = ('status', 'uploaded_at')
    search_fields = (
        'title',
        'description',
        'uploaded_by__username',
    )
    list_editable = ('status',)
    readonly_fields = ('uploaded_at', 'review_file_link')

    fields = (
        'title',
        'description',
        'file',
        'review_file_link',
        'uploaded_by',
        'uploaded_at',
        'status',
    )

    @admin.display(description='Review uploaded file')
    def review_file_link(self, obj):
        from django.urls import reverse
        from django.utils.html import format_html

        if not obj or not obj.pk or not obj.file:
            return 'No file available'

        url = reverse('resource_download', args=[obj.pk])

        return format_html(
            '<a href="{}">Open uploaded material</a>',
            url,
        )
