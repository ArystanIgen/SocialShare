from django.urls import path,include
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy
from . import views
app_name = 'blog'
urlpatterns = [
    # post views
    path('', views.dashboard, name='dashboard'),
    path('<int:blog_id>/comment',views.add_comment,name='add_comment'),
    path('create/<int:blog_id>/', views.CommentCreateView.as_view(), name='create_comment'),
]