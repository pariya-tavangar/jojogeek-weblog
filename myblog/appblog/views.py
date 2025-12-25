from django.shortcuts import render, get_object_or_404 , redirect
from .models import Post,Category,Comment
from django.utils.text import slugify
from django.core.paginator import Paginator
from .forms import CommentForm
from django.contrib import messages
from django.db.models import Sum
from django.db.models.functions import Length


def humanize_number(n):
    if n < 1000:
        return str(n)
    elif n < 1000000:
        return f"{n//1000}k"
    elif n < 1000000000:
        return f"{n//1000000}M"
    else:
        return f"{n//1000000000}B"


def home(request):
    posts = Post.objects.all().order_by('-create_at')[:2]
    recent_posts = Post.objects.all().order_by('-create_at')[:4]
    post_list = Post.objects.all().order_by('-create_at')
    paginator = Paginator(post_list, 2)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request,"home.html",{'posts':posts , 'recent_posts':recent_posts,'page_obj':page_obj})


#v4
def post_detail(request, title):
    # Find the matching post by slugified title
    posts = Post.objects.all()
    post = None
    for p in posts:
        if slugify(p.title) == title:
            post = p
            break

    # If no post found, show 404
    if not post:
        return render(request, "404.html", status=404)

    # Recent posts for sidebar
    recent_posts = Post.objects.all()[:4]

    # Only show approved top-level comments
    comments = post.comments.filter(
        approved=True,
        parent__isnull=True
    ).order_by('created_at')

    # Handle new comment or reply
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post

        # Identify admin by name (or any rule you want)
            if comment.name.lower() == "admin":  
                comment.is_admin = True

        # Check if it's a reply
        parent_id = request.POST.get('parent_id')
        if parent_id:
            comment.parent_id = parent_id

        # Still unapproved until you approve it
        comment.approved = False
        comment.save()

        messages.success(request, "Thank you for the comment ♥️ It will be shown after admin approval !")
        return redirect('post_detail', title=title)
    else:
        form = CommentForm()

    return render(request, "post_detail.html", {
        'post': post,
        'recent_posts': recent_posts,
        'comments': comments,
        'form': form,
    })


#v3
# def post_detail(request, title):
    # Find the matching post by slugified title
    # posts = Post.objects.all()
    # post = None
    # for p in posts:
    #     if slugify(p.title) == title:
    #         post = p
    #         break

    # If no post found, show 404
    # if not post:
    #     return render(request, "404.html", status=404)

    # Recent posts for sidebar
    # recent_posts = Post.objects.all()[:4]

    # Only show approved top-level comments
    # comments = post.comments.filter(
    #     approved=True,
    #     parent__isnull=True
    # ).order_by('created_at')

    # Handle new comment or reply
    # if request.method == "POST":
    #     form = CommentForm(request.POST)
    #     if form.is_valid():
    #         comment = form.save(commit=False)
    #         comment.post = post

            # Check if it's a reply
            # parent_id = request.POST.get('parent_id')
            # if parent_id:
            #     comment.parent_id = parent_id

            # Still unapproved until you approve it
            # comment.approved = False
            # comment.save()

    #         messages.success(request,"Thank you for the comment ♥ It will be shown after admin approval !")

    #         return redirect('post_detail', title=title)
    # else:
    #     form = CommentForm()

    # return render(request, "post_detail.html", {
    #     'post': post,
    #     'recent_posts': recent_posts,
    #     'comments': comments,
    #     'form': form,
    # })

#v2
# def post_detail(request, title):
#     posts = Post.objects.all()
#     post = None

#     # find the matching post by slugified title
#     for p in posts:
#         if slugify(p.title) == title:
#             post = p
#             break

#     if not post:
#         return render(request, "404.html", status=404)

#     recent_posts = Post.objects.all()[:4]
#     # comments = post.comments.filter(parent__isnull=True).order_by('-created_at')
#     comments = post.comments.filter(approved=True, parent__isnull = True).order_by('created_at')

#     # comment or reply submitted
#     if request.method == "POST":
#         form = CommentForm(request.POST)
#         if form.is_valid():
#             comment = form.save(commit=False)
#             comment.post = post

#             parent_id = request.POST.get('parent_id')
#             if parent_id:
#                 comment.parent_id = parent_id

#             comment.save()
#             return redirect('post_detail', title=title)
#     else:
#         form = CommentForm()

#     return render(request, "post_detail.html", {
#         'post': post,
#         'recent_posts': recent_posts,
#         'comments': comments,
#         'form': form,
#     })

#v1
# def post_detail(request,  title):

    posts = Post.objects.all()
    recent_posts = Post.objects.all()[:4]
    for p in posts:
        if slugify(p.title) == title:
            return render(request,"post_detail.html",{'post':p,'recent_posts':recent_posts})


def category_detail(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    posts = category.posts.all()
    return render(request, "category_detail.html", {"category": category, "posts": posts})


def about (request):

    post_count = Post.objects.count()

    char_count = Post.objects.aggregate(total = Sum(Length("content")))["total"] or 0
    word_count = char_count // 5
    word_count = humanize_number(word_count)

    comment_count = Comment.objects.count()
    comment_count = humanize_number(comment_count)
    return render(request, "about.html", {'comment_count':comment_count,"post_count": post_count, "word_count":word_count,})