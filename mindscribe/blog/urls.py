from django.urls import path
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LogoutView
from . import views
from .views import PostListView, PostDetailView, PostCreateView, PostUpdateView, PostDeleteView, UserPostsView, profile_edit

urlpatterns = [
    path('', views.home, name='home'),
    path('blog/', PostListView.as_view(), name='post_list'),
    path('blog/<int:pk>/', PostDetailView.as_view(), name='post_detail'),
    path('blog/new/', PostCreateView.as_view(), name='post_create'),
    path('blog/<int:pk>/update/', PostUpdateView.as_view(), name='post_update'),
    path('blog/<int:pk>/delete/', PostDeleteView.as_view(), name='post_delete'),
    
    # Аутентификация
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='blog/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='blog/home.html'), name='logout'),
    path('profile/', views.profile, name='profile'),
    path('profile/edit/', profile_edit, name='profile_edit'),

    path('my-posts/', UserPostsView.as_view(), name='user_posts'),
    path('post/<int:pk>/edit/', PostUpdateView.as_view(), name='post_update'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post_delete'),
    
    # Дополнительные страницы
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
]