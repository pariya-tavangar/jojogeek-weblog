from django.db import models
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField
from django.utils.html import strip_tags
import math

class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def str(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=50,unique=True)

    def __str__(self):
        return self.name


class Post(models.Model):
    title = models.CharField(max_length=200)
    content = RichTextField()
    # content = models.TextField()
    create_at = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='post_images/', blank=True,null=True)
    tags = models.ManyToManyField(Tag, related_name='posts', blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE,related_name='posts')
    # category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    category = models.ForeignKey(Category,on_delete=models.CASCADE,related_name="posts")
    read_time = models.PositiveIntegerField(default=0, editable=False)

    def save(self, *args, **kwargs):
        if self.content:
            plain_text = strip_tags(self.content)
            words = plain_text.split()
            word_count = len(words)

            self.read_time = max(1, math.ceil(word_count / 300))
        else:
            self.read_time = 1 
        super().save(*args, **kwargs)


    def __str__(self):
        return self.title



class Comment(models.Model):
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)

    name = models.CharField(max_length=100)
    body = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)
    approved = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    parent = models.ForeignKey(
        'self',
        null=True,
        blank=True,
        related_name='replies',
        on_delete=models.CASCADE
    )  # so you can reply to comments

    def str(self):
        return f'Comment by {self.name} - {self.body[:20]}'