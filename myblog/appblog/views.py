from django.shortcuts import render, get_object_or_404 , redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from django.http import JsonResponse
from django.utils.text import slugify
from django.core.paginator import Paginator
from .forms import CommentForm
from django.contrib import messages
from django.db.models import Sum
from django.db.models.functions import Length

from .models import Post, Category, Comment, Profile, SavedPost, SharedPost, Tag
from .forms import CommentForm, UserRegisterForm, UserUpdateForm, ProfileUpdateForm, PostCreateForm, SearchForm


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


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}! You can now log in.')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'register.html', {'form': form})


@login_required
def profile(request, username=None):
    if username:
        user = get_object_or_404(User, username=username)
    else:
        user = request.user
    
    posts = user.posts.all().order_by('-create_at')
    saved_posts = user.saved_posts.all().order_by('-saved_at')
    shared_posts = user.shared_posts.all().order_by('-shared_at')
    
    # Check if the current user has saved each post
    saved_post_ids = []
    if request.user.is_authenticated:
        saved_post_ids = request.user.saved_posts.values_list('post_id', flat=True)
    
    context = {
        'profile_user': user,
        'posts': posts,
        'saved_posts': saved_posts,
        'shared_posts': shared_posts,
        'is_own_profile': user == request.user,
        'saved_post_ids': list(saved_post_ids),
    }
    return render(request, 'profile.html', context)


@login_required
def profile_edit(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, 'Your profile has been updated!')
            return redirect('profile', username=request.user.username)
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)
    
    context = {
        'u_form': u_form,
        'p_form': p_form
    }
    return render(request, 'profile_edit.html', context)


@login_required
def save_post(request, post_id):
    if request.method == 'POST' or request.method == 'GET':
        post = get_object_or_404(Post, id=post_id)
        saved, created = SavedPost.objects.get_or_create(user=request.user, post=post)
        if created:
            return JsonResponse({'status': 'saved', 'message': 'Post saved!'})
        else:
            saved.delete()
            return JsonResponse({'status': 'unsaved', 'message': 'Post unsaved!'})
    return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)


@login_required
def share_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.method == 'POST':
        comment = request.POST.get('comment', '')
        shared, created = SharedPost.objects.get_or_create(
            user=request.user, 
            post=post,
            defaults={'comment': comment}
        )
        if created:
            messages.success(request, f'Post "{post.title}" shared successfully!')
        else:
            messages.info(request, f'You already shared this post')
    return redirect('post_detail', title=slugify(post.title))


@login_required
def create_post(request):
    if request.method == 'POST':
        form = PostCreateForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            form.save_m2m()  # Save many-to-many relationships (tags)
            messages.success(request, 'Post created successfully!')
            return redirect('profile', username=request.user.username)
    else:
        form = PostCreateForm()
    
    context = {
        'form': form,
    }
    return render(request, 'create_post.html', context)


@login_required
def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id, author=request.user)
    if request.method == 'POST':
        post.delete()
        messages.success(request, 'Post deleted successfully!')
        return redirect('profile', username=request.user.username)
    return render(request, 'confirm_delete.html', {'post': post})


def search_posts(request):
    form = SearchForm(request.GET or None)
    posts = Post.objects.all().order_by('-create_at')
    
    if form.is_valid():
        query = form.cleaned_data.get('query')
        category = form.cleaned_data.get('category')
        tag = form.cleaned_data.get('tag')
        
        if query:
            posts = posts.filter(title__icontains=query) | posts.filter(content__icontains=query)
        
        if category:
            posts = posts.filter(category=category)
        
        if tag:
            posts = posts.filter(tags__name__icontains=tag)
    
    paginator = Paginator(posts, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'search_results.html', {
        'form': form,
        'page_obj': page_obj,
        'posts': posts,
    })