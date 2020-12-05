from django.urls import path,include
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy
from . import views
app_name = 'images'
urlpatterns = [
    path('create/', views.image_create, name='create'),
]