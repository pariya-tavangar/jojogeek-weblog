from django.shortcuts import render, get_object_or_404
from .models import Post
from django.utils.text import slugify


def home(request):
    posts = Post.objects.all().order_by('-create_at')
    recent_posts = Post.objects.all().order_by('-create_at')[:4]
    return render(request,"home.html",{'posts':posts , 'recent_posts':recent_posts})


def post_detail(request,  title):

    posts = Post.objects.all()
    recent_posts = Post.objects.all()[:4]
    for p in posts:
        if slugify(p.title) == title:
            return render(request,"post_detail.html",{'post':p,'recent_posts':recent_posts})
