# from django import forms
# from django.contrib.auth.models import User
# from django.contrib.auth.forms import UserCreationForm
# from django.core.validators import RegexValidator
# from .models import Address
# import re

# class UserRegisterForm(UserCreationForm):
#     name = forms.CharField(max_length=100)
#     email = forms.EmailField()
#     phone_number = forms.CharField(
#         max_length=15,
#         validators=[
#             RegexValidator(
#                 regex=r'^\d{10}$',
#                 message='Phone number must be 10 digits.',
#                 code='invalid_phone'
#             )
#         ]
#     )
    
#     class Meta:
#         model = User
#         fields = ['name', 'email', 'phone_number', 'password1', 'password2']
    
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         # Add Bootstrap classes to form fields
#         for field_name in self.fields:
#             self.fields[field_name].widget.attrs.update({'class': 'form-control'})
    
#     def clean_password1(self):
#         password = self.cleaned_data.get('password1')
#         if password:
#             # Check password length
#             if len(password) < 8:
#                 raise forms.ValidationError("Password must be at least 8 characters long.")
            
#             # Check for uppercase
#             if not any(c.isupper() for c in password):
#                 raise forms.ValidationError("Password must contain at least one uppercase letter.")
            
#             # Check for lowercase
#             if not any(c.islower() for c in password):
#                 raise forms.ValidationError("Password must contain at least one lowercase letter.")
            
#             # Check for digit
#             if not any(c.isdigit() for c in password):
#                 raise forms.ValidationError("Password must contain at least one number.")
            
#             # Check for special character
#             if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
#                 raise forms.ValidationError("Password must contain at least one special character.")
        
#         return password

#     def save(self, commit=True):
#         user = super().save(commit=False)
#         user.username = self.cleaned_data['email']
#         user.email = self.cleaned_data['email']
#         user.first_name = self.cleaned_data['name']
        
#         if commit:
#             user.save()
#         return user

# class UserUpdateForm(forms.ModelForm):
#     name = forms.CharField(max_length=100)
#     email = forms.EmailField()
#     phone_number = forms.CharField(
#         max_length=15,
#         validators=[
#             RegexValidator(
#                 regex=r'^\d{10}$',
#                 message='Phone number must be 10 digits.',
#                 code='invalid_phone'
#             )
#         ]
#     )

#     class Meta:
#         model = User
#         fields = ['name', 'email', 'phone_number']

#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         # Add Bootstrap classes to form fields
#         for field_name in self.fields:
#             self.fields[field_name].widget.attrs.update({'class': 'form-control'})
        
#         if self.instance:
#             self.fields['name'].initial = self.instance.first_name
#             self.fields['email'].initial = self.instance.email
#             # Phone number would be stored in profile or as a separate field

#     def save(self, commit=True):
#         user = super().save(commit=False)
#         user.username = self.cleaned_data['email']
#         user.email = self.cleaned_data['email']
#         user.first_name = self.cleaned_data['name']
        
#         if commit:
#             user.save()
#         return user

# class AddressForm(forms.ModelForm):
#     class Meta:
#         model = Address
#         fields = ['house_street', 'landmark', 'pincode', 'state']
#         widgets = {
#             'house_street': forms.TextInput(attrs={'class': 'form-control'}),
#             'landmark': forms.TextInput(attrs={'class': 'form-control'}),
#             'pincode': forms.TextInput(attrs={'class': 'form-control'}),
#             'state': forms.TextInput(attrs={'class': 'form-control'}),
#         }

# class SubscriptionForm(forms.Form):
#     email = forms.EmailField(
#         widget=forms.EmailInput(attrs={
#             'class': 'form-control',
#             'placeholder': 'Enter your email'
#         })
#     )


from django import forms
from django.contrib.auth.models import User
from .models import Address

class UserRegisterForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput)
    
    class Meta:
        model = User
        fields = ['first_name', 'email']
        
    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError('Passwords do not match')
        return password2

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'email']
        labels = {
            'first_name': 'Name',
        }

class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ['name', 'house_street', 'city', 'state', 'pincode']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Address Name (e.g. Home, Work)'}),
            'house_street': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'House/Apartment No., Street'}),
            'city': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'City'}),
            'state': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'State'}),
            'pincode': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Pincode'}),
        }
