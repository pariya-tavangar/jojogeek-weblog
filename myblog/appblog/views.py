from django.shortcuts import render, get_object_or_404 , redirect
from .models import Post,Category,Comment
from django.utils.text import slugify
from django.core.paginator import Paginator
from .forms import CommentForm


def home(request):
    posts = Post.objects.all().order_by('-create_at')[:2]
    recent_posts = Post.objects.all().order_by('-create_at')[:4]
    post_list = Post.objects.all().order_by('-create_at')
    paginator = Paginator(post_list, 2)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request,"home.html",{'posts':posts , 'recent_posts':recent_posts,'page_obj':page_obj})


def post_detail(request, title):
    posts = Post.objects.all()
    post = None

    # find the matching post by slugified title
    for p in posts:
        if slugify(p.title) == title:
            post = p
            break

    if not post:
        return render(request, "404.html", status=404)

    recent_posts = Post.objects.all()[:4]
    comments = post.comments.filter(parent__isnull=True).order_by('-created_at')

    # comment or reply submitted
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post

            parent_id = request.POST.get('parent_id')
            if parent_id:
                comment.parent_id = parent_id

            comment.save()
            return redirect('post_detail', title=title)
    else:
        form = CommentForm()

    return render(request, "post_detail.html", {
        'post': post,
        'recent_posts': recent_posts,
        'comments': comments,
        'form': form,
    })



# def post_detail(request,  title):

#     posts = Post.objects.all()
#     recent_posts = Post.objects.all()[:4]
#     for p in posts:
#         if slugify(p.title) == title:
#             return render(request,"post_detail.html",{'post':p,'recent_posts':recent_posts})


def category_detail(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    posts = category.posts.all()
    return render(request, "category_detail.html", {"category": category, "posts": posts})