from django.urls import path,include
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy
from . import views
from django.contrib.auth.decorators import login_required
from .models import Blog,Comment,LikeDislike
app_name = 'blog'
urlpatterns = [
    # post views
    path('', views.dashboard, name='dashboard'),
    path('<int:blog_id>/comment',views.add_comment,name='add_comment'),
    path('blog/<pk>/like/',views.like, name='like'),
    path('blog/<pk>/delete/',views.blog_delete, name='blog_delete'),
    path('blog/<pk>/dislike/',views.dislike, name='dislike'),
    path('search/', views.user_search, name='user_search'),
    ]