from django.contrib import admin
from .models import Post, Tag, Category ,Comment
   
admin.site.register(Post)
admin.site.register(Tag)
admin.site.register(Category)
@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("name", "post", "approved", "created_at")
    list_filter = ("approved", "created_at")
    search_fields = ("name", "body")