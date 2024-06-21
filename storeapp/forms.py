from django import forms
from django.forms import ModelForm
#from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from userapp.models import User
from storeapp.models import ProductReview,Address

# PRODUCT REVIEW PLACEMENT


class ProductReviewForm(forms.ModelForm):
    review = forms.CharField(widget=forms.Textarea(attrs={'placeholder': "Write review",
                                                          "class": "textarea", "rows": 6, "cols": 20,
                                                          }))

    class Meta:
        model = ProductReview
        fields = ['review', 'rating']


class AddressForm(ModelForm):
    class Meta:
        model = Address
        fields = ['address', 'status']


class UpdateUserForm(ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']
