from django.http import HttpResponseRedirect
from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Blog,Comment
from .forms import BlogForm,CommentForm,CommentModelForm
from bootstrap_modal_forms.generic import BSModalCreateView
from django.urls import reverse_lazy

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
class CommentCreateView(BSModalCreateView):
    template_name = 'blog/comment.html'
    form_class = CommentModelForm
    success_message = 'Success: Comment was created.'
    success_url = reverse_lazy('blog:dashboard')