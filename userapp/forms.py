from django import forms
from userapp.models import User, Profile
#from django.contrib.auth.models import User
from storeapp.models import Vendor, Product
from django.contrib.auth.forms import UserCreationForm


class RegistrationForm(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput(
        attrs={"placeholder": "Username"}))
    firstname = forms.CharField(widget=forms.TextInput(
        attrs={"placeholder": "Firstname"}))
    lastname = forms.CharField(widget=forms.TextInput(
        attrs={"placeholder": "Lastname"}))
    email = forms.EmailField(widget=forms.EmailInput(
        attrs={"Placeholder": "Email"}), required=True)
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Enter Password',
        'class': 'form-control'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Confirm Password'}))

    class Meta:
        model = User
        fields = [
            'username',
            'email',
            # 'phone_number',
        ]

class ProfileForm(forms.ModelForm):
    full_name = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "Username"}))
    bio = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'bio'}))
    phone = forms.CharField(widget=forms.TextInput(attrs={'Placeholder':'phone'}))

    class Meta:
        model = Profile
        fields = ['full_name', 'bio', 'phone', 'image']


# TO REGISTER AS VENDOR
class VendorRegistrationForm(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "Company Name"}))
    description = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Description'}))

    class Meta:
        model = Vendor
        fields = ['name', 'description', 'image', 'cover_image']  



class VendorNewItemForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ["category", "name", "price", "old_price","picture", "slug","vendor", "vendor_product"]      
    
        widgets = {
            'name': forms.TextInput(attrs={
                'class':"input-class",
                'placeholder': "product name"
            }),
            'category' : forms.Select(attrs={
                "class": "input-class",
            }),
            'price' : forms.TextInput(attrs={
                'class': "input-class",
                "placeholder": "price"
            }),
            'old_price' : forms.TextInput(attrs={
                'class': "input-class",
                "placeholder": "old price"
            }),
            'picture' : forms.FileInput(attrs={
                'class': 'image-input'
            }),
            'slug' : forms.TextInput(attrs={
                'class': "input-class",
                "placeholder": "slug"
            }),
            'vendor' : forms.Select(attrs={
                "class": "input-class",
            }),

        }



class EditProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ('name', 'price', 'picture', 'in_stock')
        widgets = {
            'name': forms.TextInput(attrs={
                'class':"input-class",
                'placeholder': "product name"
            }),
            'price' : forms.TextInput(attrs={
                'class': "input-class",
                "placeholder": "price"
            }),
            'picture' : forms.FileInput(attrs={
                'class': 'image-input'
            }),

        }        


    
