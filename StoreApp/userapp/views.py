from django.shortcuts import render
import json
import uuid
from django.shortcuts import render, redirect
from django.http import HttpResponse
from . forms import RegistrationForm, ProfileForm, VendorRegistrationForm
from storeapp.models import Cart, CartItem, Vendor
# To be able to use the user function at (myuser(variable)
#from django.contrib.auth.models import User
from userapp.models import User, Profile, OtpToken
from django.contrib import messages, auth
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required


# Verification email
#EMAIL ACTIVATION IMPORTS
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.core.mail import send_mail
'''
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage
'''


# IMPORT FOR CHANGE PASSWORD FUNCTION
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash



# Create your views here.

# SIGN UP VIEW
def register_view(request):
    if request.user.is_authenticated:
        messages.warning(
            request, f"Hey {request.user} you are already logged in.")
        return redirect('storeapp:home')

    if request.method == 'POST':
        form = RegistrationForm(request.POST or None)
        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.save()
            # WE USE CLEANED DATA TO FETCH ALL VALUES FROM THE REQUEST
            username = form.cleaned_data['firstname']

            messages.success(request, f"Hey {username}, your account was created successfully. An OTP was sent to your Email")
            return redirect("userapp:verify-email", username=request.POST['username'])

            #new_user = User.objects.create_user(first_name=first_name, last_name=last_name, email=email, password=password)
            #new_user = User.objects.create_user(email=form.cleaned_data['email'])
            #new_user.save()
        

            """
            new_user = authenticate(username=form.cleaned_data['email'], 
                                    password=form.cleaned_data['password1'])
            login(request, new_user)

            Profile.objects.create(user=request.user)

            return redirect('storeapp:home')
            """
        else:
            for error in list(form.errors.values()):
                messages.error(request, error)

    else:
        form = RegistrationForm()

    context = {
        'form': form
    }
    return render(request, 'signup.html', context)






#EMAIL VERIFICATION WITH OTP ACTIVATION TOKEN
def verify_email(request, username):
    user = get_user_model().objects.get(username=username)
    user_otp = OtpToken.objects.filter(user=user).last()
    
    
    if request.method == 'POST':
        # valid token
        if user_otp.otp_code == request.POST['otp_code']:
            
            # checking for expired token
            if user_otp.otp_expires_at > timezone.now():
                user.is_active=True
                user.save()
                messages.success(request, "Account activated successfully!! You can Login.")
                return redirect("userapp:login")
            
            # expired token
            else:
                messages.warning(request, "The OTP has expired, get a new OTP!")
                return redirect("userapp:verify-email", username=user.username)
        
        
        # invalid otp code
        else:
            messages.warning(request, "Invalid OTP entered, enter a valid OTP!")
            return redirect("userapp:verify-email", username=user.username)
        
    context = {}
    return render(request, "authentication/verify_token.html", context)







# RESEND OTP IF PREV OTP HAS EXPIRED
def resend_otp(request):
    if request.method == 'POST':
        user_email = request.POST["otp_email"]
        
        if get_user_model().objects.filter(email=user_email).exists():
            user = get_user_model().objects.get(email=user_email)
            otp = OtpToken.objects.create(user=user, otp_expires_at=timezone.now() + timezone.timedelta(minutes=5))
            
            
            # email variables
            subject="Email Verification"
            message = f"""
                                Hi {user.username}, here is your OTP {otp.otp_code} 
                                it expires in 5 minute, use the url below to redirect back to the website
                                http://127.0.0.1:8000/verify-email/{user.username}
                                
                                """
            sender = "MYKE Stores"
            receiver = [user.email, ]
        
        
            # send email
            send_mail(
                    subject,
                    message,
                    sender,
                    receiver,
                    fail_silently=False,
                )
            
            messages.success(request, "A new OTP has been sent to your email-address")
            return redirect("userapp:verify-email", username=user.username)

        else:
            messages.warning(request, "This email dosen't exist in the database")
            return redirect("userapp:resend-otp")
        
           
    context = {}
    return render(request, "authentication/resend_otp.html", context)







# TO ASSIGN CART TO LOGGED IN USER
def login_view(request):
    if request.user.is_authenticated:
        messages.warning(
            request, f"Hey {request.user} you are already logged in.")
        return redirect('storeapp:home')

    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        try:
            user = User.objects.get(email=email)
        except:
            messages.warning(request, f"User with {email} already exists ☹")    
            
        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user)
            print(request.user.username)

            try:
                cart = Cart.objects.get(
                    session_id=request.session["nonuser"], completed=False)
                if Cart.objects.filter(user=request.user, completed=False).exists():
                    cart.user = None
                    cart.save()

                else:
                    cart.user = request.user
                    cart.save()

            except:
                print("Not available")

            messages.success(request, "You are now logged in")
            return redirect("storeapp:home")
            

        else:
            messages.error(request, "User does not exist ☹, create an account.")
            return redirect('userapp:login')
    return render(request, 'login.html')


@login_required(login_url='login')
def logout(request):
    auth.logout(request)
    messages.success(request, 'You are logged out')
    return redirect('userapp:login')


# DASHBOARD VIEW
@login_required(login_url='login')
def dashboard(request):
    return render(request, "dashboard.html")

# END OF REGULAR USER AUTHENTICATION





# FORGOT PASSWORD
def forgotPassword(request):
    return render(request, "forgotPassword.html")




#CHANGE PASSWORD
@login_required(login_url='login')
def change_password(request):
    #CHECKING IF USER EXISTS IN GROUP 
    if request.method == "POST":
        form=PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            messages.success(request, "Your password has been changed successfully....")
            return redirect("storeapp:settings")
    else:
        form = PasswordChangeForm(user=request.user)
    

    context ={
        'form':form,
    }    

    return render(request, "change_password.html", context)





#EDIT PROFILE AT DASHBOARD
def profile_update(request):
    profile = Profile.objects.get(user=request.user)
    try:
        user_profile = Profile.objects.get(user=request.user)
    except:
        user_profile = Profile.objects.create(
                user=request.user
            ) 
    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            new_form = form.save(commit=False)
            new_form.user = request.user
            new_form.save()
            messages.success(request, "Profile updated successfully")
            return redirect("storeapp:dashboard")
    else:
        form = ProfileForm(instance=profile)

    context = {
        "form":form,
        "profile":profile,
        "user_profile":user_profile
    }        

    return render(request, 'profile-update.html', context)



def vendor_application(request):
    try:
        profile = Profile.objects.get(user=request.user)
    # for anonymous users trying to reg as vendor
    except TypeError:
        messages.error(request, "Login to continue with vendor application")
        return redirect("storeapp:vendors")

    if request.method == "POST":
        form = VendorRegistrationForm(request.POST, request.FILES or None)
        if form.is_valid():
            #new_user = form.save(commit = False)
            #new_user.user = profile.user
            #new_user.save()
            name = form.cleaned_data['name']
            image = form.cleaned_data['image']
            cover_image = form.cleaned_data['cover_image']
            profile.image = image
            profile.full_name = name
            profile.cover_image = cover_image
            vendor = Vendor.objects.create(
                name = profile.full_name,
                title = profile.full_name,
                image = profile.image,
                cover_image = profile.cover_image,
                user = profile.user
                )
            vendor.save()
            messages.success(request, f"Hey {request.user} your vendor name '{vendor.name}' has been created successfully")
            return redirect("storeapp:vendors")

    else:
        form = VendorRegistrationForm()
    context ={
        "form":form,
        #"profile":profile
    }            
    return render(request, "vendor-application.html", context)