from django.db import models
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField
from django.utils.html import strip_tags
from django.db.models.signals import post_save
from django.dispatch import receiver
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
    

# ===== NEW PROFILE MODELS =====

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField(max_length=500, blank=True, null=True)
    image = models.ImageField(upload_to='profile_images/', default='default_profile.jpg', blank=True)
    banner = models.ImageField(upload_to='banner_images/', blank=True, null=True)
    website = models.URLField(blank=True, null=True)
    location = models.CharField(max_length=100, blank=True, null=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"


class SavedPost(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='saved_posts')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='saved_by')
    saved_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'post')  # Prevent duplicate saves

    def __str__(self):
        return f"{self.user.username} saved {self.post.title}"


class SharedPost(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='shared_posts')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='shared_by')
    shared_at = models.DateTimeField(auto_now_add=True)
    comment = models.TextField(blank=True, null=True)

    class Meta:
        unique_together = ('user', 'post')

    def __str__(self):
        return f"{self.user.username} shared {self.post.title}"


# ===== SIGNALS TO AUTO-CREATE PROFILE =====

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()