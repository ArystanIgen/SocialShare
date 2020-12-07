from django.urls import path,include
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy
from . import views
app_name = 'users'
urlpatterns = [
    # post views
    path('login/', views.user_login, name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='account/logged_out.html'), name='logout'),
    path('logout-then-login/', auth_views.logout_then_login, name='logout_then_login'),
    path('password-change/', auth_views.PasswordChangeView.as_view(template_name='account/password_change_form.html',success_url=reverse_lazy('users:password_change_done')), name='password_change'),
    path('password-change/done/', auth_views.PasswordChangeDoneView.as_view(template_name='account/password_change_done.html'), name='password_change_done'),
    # restore password urls
    path('password-reset/', auth_views.PasswordResetView.as_view(template_name='account/password_reset_form.html',
                                                                 email_template_name='account/password_reset_email.html',
                                                                 success_url=reverse_lazy('users:password_reset_done'),

                                                                ), name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='account/password_reset_done.html',), name='password_reset_done'),
    path('password_reset_<uidb64>_<token>/', auth_views.PasswordResetConfirmView.as_view(
                                template_name='account/password_reset_confirm.html',
                                success_url=reverse_lazy('users:password_reset_complete'),
    ), name='password_reset_confirm'),
    path('password-reset/complete/',auth_views.PasswordResetCompleteView.as_view(template_name='account/password_reset_complete.html'), name='password_reset_complete'),
    path('register-complete/',views.registration_c,name='registration_c'),
    path('edit/', views.edit, name='edit'),
    path('profile/', views.profile, name='profile'),
    path('users/<username>',views.others,name='others'),
    path('users/', views.user_list, name='user_list'),
    path('users/follow/', views.user_follow, name='user_follow'),
]