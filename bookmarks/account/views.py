from django.http import HttpResponse,Http404
from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth import authenticate, login
from .models import Profile
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .forms import LoginForm, UserRegistrationForm, UserEditForm, ProfileEditForm,Search1Form
from django.contrib import messages
from blog.models import Blog,Comment
from haystack.query import SearchQuerySet
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from common.decorators import ajax_required
from .models import Contact

def registration_c(request):
    return render(request, 'account/register_done.html')
def user_login(request):
        s_form=Search1Form()
        form = LoginForm(request.POST or None)
        user_form = UserRegistrationForm(request.POST or None)
        if request.method == 'POST':
            if request.POST.get('submit') == 'Log-in':

                if form.is_valid():
                    cd = form.cleaned_data
                    user = authenticate(username=cd['username'], password=cd['password'])
                    if user is not None:
                        if user.is_active:
                            login(request, user)
                            return redirect('blog:dashboard')
                        else:
                            return HttpResponse('Disabled account')
                    else:
                        return HttpResponse('Invalid login')
            elif request.POST.get('submit') == 'Create my account':
                if user_form.is_valid():
                    # Create a new user object but avoid saving it yet
                    new_user = user_form.save(commit=False)
                    # Set the chosen password
                    new_user.set_password(user_form.cleaned_data['password'])
                    # Save the User object
                    new_user.save()
                    profile = Profile.objects.create(user=new_user)
                    return render(request, 'account/register_done.html', {'new_user': new_user,"s_form":s_form})
        context = {
            'form':form,
            'user_form': user_form
        }
        return render(request, 'account/login.html', context)
@login_required
def edit(request):
    s_form = Search1Form()
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user, data=request.POST)
        profile_form = ProfileEditForm(instance=request.user.profile, data=request.POST, files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Profile updated successfully')
        else:
            messages.error(request, 'Error updating your profile')
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)
    return render(request,
                  'account/edit.html',
                  {'user_form': user_form,
                   'profile_form': profile_form,
                   "s_form":s_form})
@login_required
def profile(request):
        s_form = Search1Form()
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)
        blogs = Blog.objects.filter(user=request.user).order_by('date_added')
        return render(request,
                      'account/profile.html',
                      {'user_form': user_form,
                       'profile_form': profile_form,
                       'blogs':blogs,
                       's_form':s_form
                       })
@login_required
def others(request,username):
    s_form = Search1Form()
    try:
        user = User.objects.get(username=username)
    except:
        raise Http404

        # Flag that determines if we should show editable elements in template
    blogs = Blog.objects.filter(user=user).order_by('date_added')
    context = locals()
    template = 'account/others.html'
    return render(request, template, context)

@login_required
def user_list(request):
    s_form = Search1Form()
    users = User.objects.filter(is_active=True)
    return render(request,
                  'users/users_list.html',
                  {'section': 'people',
                   'users': users,
                   's_form':s_form})


@ajax_required
@require_POST
@login_required
def user_follow(request):
    user_id = request.POST.get('id')
    action = request.POST.get('action')
    if user_id and action:
        try:
            user = User.objects.get(id=user_id)
            if action == 'follow':
                Contact.objects.get_or_create(user_from=request.user,
                                              user_to=user)

            else:
                Contact.objects.filter(user_from=request.user,
                                       user_to=user).delete()
            return JsonResponse({'status':'ok'})
        except User.DoesNotExist:
            return JsonResponse({'status':'error'})
    return JsonResponse({'status':'error'})