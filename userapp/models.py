from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete
import uuid  # TO USE UUID
from django.db.models.signals import post_save
from storeapp.models import *
import secrets



# Create your models here.


class User(AbstractUser):
    username = models.CharField(max_length=100, unique=True)
    email = models.EmailField(unique=True)
    bio = models.CharField(max_length=600)

    # REQUIRED
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now_add=True)
    is_superuser = models.BooleanField(default=False)
    is_vendor = models.BooleanField(default=False)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.username




#OTP Model
class OtpToken(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="otps")
    otp_code = models.CharField(max_length=6, default=secrets.token_hex(3))
    otp_created_at = models.DateTimeField(auto_now_add=True)
    otp_expires_at = models.DateTimeField(blank=True, null=True)
    
    
    def __str__(self):
        return self.user.username
    



class ContactUs(models.Model):
    full_name = models.CharField(max_length=200)
    email = models.EmailField()
    phone = models.CharField(max_length=200)
    subject = models.CharField(max_length=300)
    message = models.TextField()

    class Meta:
        verbose_name_plural = "Contact Us"

    def __str__(self):
        return self.full_name


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    image = models.ImageField(upload_to="image")
    full_name = models.CharField(max_length=200, null=True, blank=True)
    bio = models.CharField(max_length=300, null=True, blank=True)
    phone = models.CharField(max_length=200)
    verified = models.BooleanField(default=False)
    #review = models.ForeignKey("storeapp.ProductReview", on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.user.username

# USING SIGNALS TO AUTO SAVE THE CREATED USER PROFILE ABOVE
def create_user_profile(sender, instance, created, **kwargs):
    # refering to the created argument above
    if created:
        Profile.objects.create(user=instance)  # instance of User class

    # Func to save
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()

    # Connects d created profile instance of User
    post_save.connect(create_user_profile, sender=User)

    # Saves the connected new user
    post_save.connect(save_user_profile, sender=User)


