from django.contrib import admin
from .models import Post, Tag
from .models import Category

admin.site.register(Post)
admin.site.register(Tag)
admin.site.register(Category)