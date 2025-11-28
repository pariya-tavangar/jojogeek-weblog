from django.db import models
from django.contrib.auth.models import User


class Tag(models.Model):
    name = models.CharField(max_length=50,unique=True)

    def __str__(self):
        return self.name


class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    create_at = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='post_images/', blank=True,null=True)
    tags = models.ManyToManyField(Tag, related_name='posts', blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE,related_name='posts')


    def __str__(self):
        return self.title

