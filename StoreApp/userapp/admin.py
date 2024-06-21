from django.contrib import admin
from .models import User, Profile, ContactUs, OtpToken


# Register your models here.

class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'bio']


admin.site.register(User)
admin.site.register(Profile)
admin.site.register(ContactUs)
admin.site.register(OtpToken)