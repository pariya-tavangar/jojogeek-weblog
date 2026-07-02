from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('',views.home, name='home'),
    path('post/<str:title>/', views.post_detail, name='post_detail'),
    path('category/<int:category_id>/', views.category_detail, name="category_detail"),
    path('about/', views.about, name='about'),

 # ========== NEW AUTHENTICATION URLs ==========
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='logout.html'), name='logout'),
    
    # ========== NEW PROFILE URLs ==========
    path('profile/', views.profile, name='profile'),
    path('profile/<str:username>/', views.profile, name='profile'),
    path('profile/edit/', views.profile_edit, name='profile_edit'),
    
    # ========== NEW POST MANAGEMENT URLs ==========
    path('post/create/', views.create_post, name='create_post'),
    path('post/<int:post_id>/delete/', views.delete_post, name='delete_post'),
    
    # ========== NEW POST INTERACTION URLs ==========
    path('post/<int:post_id>/save/', views.save_post, name='save_post'),
    path('post/<int:post_id>/share/', views.share_post, name='share_post'),
    
    # ========== NEW SEARCH URL ==========
    path('search/', views.search_posts, name='search_posts'),
]