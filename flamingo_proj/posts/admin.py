from django.contrib import admin

from .models import Post, Tag, Like


class PostModelAdmin(admin.ModelAdmin):
    list_display = ['content', 'created', 'posted_by']
    search_fields = ['content']

    class Meta:
        model = Post


class TagModelAdmin(admin.ModelAdmin):
    search_fields = ['tag']

    class Meta:
        model = Tag


admin.site.register(Post, PostModelAdmin)
admin.site.register(Tag, TagModelAdmin)
admin.site.register(Like)
