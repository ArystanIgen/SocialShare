from django.http import HttpResponseRedirect,HttpResponse
from django.views import View
from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Blog,Comment,LikeDislike
from account.models import Profile
from .forms import BlogForm,CommentForm,Search1Form
from django.urls import reverse_lazy
from django.contrib.contenttypes.models import ContentType
import json
from itertools import chain
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.contrib.auth.models import User
from haystack.query import SearchQuerySet
@login_required
def dashboard(request):
    """Определяет новую тему."""
    s_form = Search1Form()
    users = User.objects.filter(is_active=True)
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
    latest_post_list=Blog.objects.order_by('-date_added')[:365]
    return render(request, 'blog/dashboard.html', {'users':users,'latest_post_list':latest_post_list,'form':form,'s_form':s_form})
@login_required
def add_comment(request,blog_id):
    s_form = Search1Form()
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
    context={'c_form':c_form,"blog":blog,'s_form':s_form}
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


def user_search(request):
    form = Search1Form()
    cd=None
    results=[]
    total_results=None
    if 'query' in request.GET:
        form = Search1Form(request.GET)
        if form.is_valid():
            cd = form.cleaned_data
            results = SearchQuerySet().models(User).filter(content=cd['query']).load_all()
            # count total results
            total_results = results.count()
    return render(request,
                  'blog/search.html',
                  {'s_form': form,
                   'cd': cd,
                   'results': results,
                   'total_results': total_results})


def blog_delete(request, pk):
    blog = get_object_or_404(Blog, pk=pk)
    blog.delete()
    return redirect('users:profile')