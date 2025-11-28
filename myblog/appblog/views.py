from django.shortcuts import render, get_object_or_404
from .models import Post
from django.utils.text import slugify
from django.core.paginator import Paginator


def home(request):
    posts = Post.objects.all().order_by('-create_at')[:2]
    recent_posts = Post.objects.all().order_by('-create_at')[:4]
    post_list = Post.objects.all().order_by('-create_at')
    paginator = Paginator(post_list, 2)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request,"home.html",{'posts':posts , 'recent_posts':recent_posts,'page_obj':page_obj})


def post_detail(request,  title):

    posts = Post.objects.all()
    recent_posts = Post.objects.all()[:4]
    for p in posts:
        if slugify(p.title) == title:
            return render(request,"post_detail.html",{'post':p,'recent_posts':recent_posts})
