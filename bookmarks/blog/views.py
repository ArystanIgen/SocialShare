from django.http import HttpResponseRedirect,HttpResponse
from django.views import View
from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Blog,Comment,LikeDislike
from .forms import BlogForm,CommentForm,CommentModelForm
from bootstrap_modal_forms.generic import BSModalCreateView
from django.urls import reverse_lazy
from django.contrib.contenttypes.models import ContentType
import json
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.decorators import method_decorator
@login_required
def dashboard(request):
    """Определяет новую тему."""
    if request.method != 'POST':
        form = BlogForm()

        # Данные не отправились
    else:
        # Отправлены данные POST; обработать данные
        form = BlogForm(request.POST,request.FILES)
        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.user=request.user
            new_post.save()
            return redirect('blog:dashboard')
    # Вывести пустую или не действительную строку
    latest_post_list=Blog.objects.order_by('-date_added')[:5]
    return render(request, 'blog/dashboard.html', {'latest_post_list':latest_post_list,'form':form,})
@login_required
def add_comment(request,blog_id):

    blog=Blog.objects.get(id=blog_id)

    if request.method!='POST':
        c_form = CommentForm()
        #Данные не отправились
    else:
        #Отправлены данные POST; обработать данные
        c_form = CommentForm(data=request.POST)
        
        if c_form.is_valid():
            new_comment = c_form.save(commit=False)
            new_comment.blog = blog
            new_comment.comment_user=request.user
            new_comment.save()
            return HttpResponseRedirect('/')
    #Вывести пустую или не действительную строку
    context={'c_form':c_form,"blog":blog}
    return render(request, 'blog/comment.html', context)


def like(request, pk):
    obj = Blog.objects.get(pk=pk)
    try:
        likedislike = LikeDislike.objects.get(content_type=ContentType.objects.get_for_model(obj), object_id=obj.id,
                                              user=request.user)
        if likedislike.vote is not LikeDislike.LIKE:
            likedislike.vote = LikeDislike.LIKE
            likedislike.save(update_fields=['vote'])
            result = True
        else:
            likedislike.delete()
            result = False
    except LikeDislike.DoesNotExist:
        obj.votes.create(user=request.user, vote=LikeDislike.LIKE)
        result = True

    return HttpResponse(
        json.dumps({
            "result": result,
            "like_count": obj.votes.likes().count(),
            "dislike_count": obj.votes.dislikes().count(),
            "sum_rating": obj.votes.sum_rating()
        }),
        content_type="application/json"
    )

def dislike(request, pk):
    obj = Blog.objects.get(pk=pk)
    try:
        likedislike = LikeDislike.objects.get(content_type=ContentType.objects.get_for_model(obj), object_id=obj.id,
                                              user=request.user)
        if likedislike.vote is not LikeDislike.DISLIKE:
            likedislike.vote = LikeDislike.DISLIKE
            likedislike.save(update_fields=['vote'])
            result = True
        else:
            likedislike.delete()
            result = False
    except LikeDislike.DoesNotExist:
        obj.votes.create(user=request.user, vote=LikeDislike.DISLIKE)
        result = True

    return HttpResponse(
        json.dumps({
            "result": result,
            "like_count": obj.votes.likes().count(),
            "dislike_count": obj.votes.dislikes().count(),
            "sum_rating": obj.votes.sum_rating()
        }),
        content_type="application/json"
    )