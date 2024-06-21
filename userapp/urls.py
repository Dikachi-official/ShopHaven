from django.urls import path, reverse_lazy
from . import views
from django.contrib.auth import views as auth_views

app_name = "userapp"

urlpatterns = [
    # SIGNUP URL
    path('signup', views.register_view, name='signup'),

    #LOGIN URL
    path('login', views.login_view, name='login'),

    #LOGOUT URL
    path('signout', views.logout, name='signout'),

    #EMAIL ACTIVATION VERIFICATION
    path("verify-email/<slug:username>", views.verify_email, name="verify-email"),
    path("resend-otp", views.resend_otp, name="resend-otp"),

    # DASHBOARD URL
    path('dashboard', views.dashboard, name="dashboard"),

    #CHANGE PASSWORD
    path('changepassword/', views.change_password, name='change-password'),

    # UPDATE VENDOR-USER-PROFILE VIEW
    path('profile/update', views.profile_update, name='profile-update'),
    
    # VENDOR APPLICATION URL
    path('vendor-application', views.vendor_application, name='vendor-application'),
    

    #path('forgotPassword', views.forgotPassword, name='forgotPassword'),
    #path('resetpassword_validate/<uidb64>/<token>/',views.resetpassword_validate, name='resetpassword_validate'),
    #path('resetPassword', views.resetPassword, name="resetPassword")
    #path('changeaddress', views.changeaddress, name='changeaddress')

    # PASSWORD RESET URLS
    path('password_reset/', auth_views.PasswordResetView.as_view(
        template_name='password_reset_form.html', 
        email_template_name='password_reset_email.html',
        success_url=reverse_lazy('userapp:password_reset_done')), 
        name='password_reset'),
        
    path('password_reset_done/', auth_views.PasswordResetDoneView.as_view(template_name='password_reset_done.html', ), name='password_reset_done'),

    path('password_reset_confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='password_reset_confirm.html', 
        success_url=reverse_lazy('userapp:password_reset_complete', )), 
        name='password_reset_confirm'),

    path('password_reset_complete/', auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html', ), name='password_reset_complete'),
]
