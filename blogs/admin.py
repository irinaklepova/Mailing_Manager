from django.contrib import admin

from blogs.models import Blog


@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'is_published', 'views_count',)
    list_filter = ('is_published', 'views_count', 'created_at')
    search_fields = ('title', 'body',)
