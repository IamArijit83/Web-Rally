from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.landing, name='landing'),  # ✅ root path → landing

    path('home/', views.home, name='home'),   # ✅ dashboard after login
    path('details/', views.user_details, name='user_details'),

    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),


    path('history/', views.history_view, name='history'),
    path('analytics/', views.analytics_view, name='analytics'),
    path('feedback/', views.feedback_view, name='feedback'),

    # Password reset URLs (optional)
    path('password-reset/', auth_views.PasswordResetView.as_view(
        template_name='tracker/password_reset.html'), name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(
        template_name='tracker/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='tracker/password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(
        template_name='tracker/password_reset_complete.html'), name='password_reset_complete'),
]
