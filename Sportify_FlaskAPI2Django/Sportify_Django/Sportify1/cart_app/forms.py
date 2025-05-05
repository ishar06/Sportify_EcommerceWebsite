from django import forms
from django.core.validators import RegexValidator
from .models import Product, Category, Subscription

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['category', 'title', 'description', 'price', 'stock', 'image']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
            'stock': forms.NumberInput(attrs={'class': 'form-control'}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
        }

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'slug', 'image']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'slug': forms.TextInput(attrs={'class': 'form-control'}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
        }

class CheckoutForm(forms.Form):
    PAYMENT_CHOICES = (
        ('card', 'Credit/Debit Card'),
        ('cod', 'Cash on Delivery'),
    )
    
    payment_method = forms.ChoiceField(
        choices=PAYMENT_CHOICES,
        widget=forms.RadioSelect(attrs={'class': 'form-check-input'})
    )
    
    # Card details
    card_number = forms.CharField(
        required=False,
        max_length=19,  # 16 digits + 3 spaces
        validators=[
            RegexValidator(
                regex=r'^\d{16}$',
                message='Card number must be 16 digits.',
                code='invalid_card'
            )
        ],
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '1234 5678 9012 3456'})
    )
    
    expiry_date = forms.CharField(
        required=False,
        max_length=5,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'MM/YY'})
    )
    
    cvv = forms.CharField(
        required=False,
        max_length=3,
        validators=[
            RegexValidator(
                regex=r'^\d{3}$',
                message='CVV must be 3 digits.',
                code='invalid_cvv'
            )
        ],
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '123'})
    )
    
    card_name = forms.CharField(
        required=False,
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    
    def clean(self):
        cleaned_data = super().clean()
        payment_method = cleaned_data.get('payment_method')
        
        if payment_method == 'card':
            card_number = cleaned_data.get('card_number')
            expiry_date = cleaned_data.get('expiry_date')
            cvv = cleaned_data.get('cvv')
            card_name = cleaned_data.get('card_name')
            
            if not all([card_number, expiry_date, cvv, card_name]):
                raise forms.ValidationError('All card details are required.')
        
        return cleaned_data

class SubscriptionForm(forms.ModelForm):
    class Meta:
        model = Subscription
        fields = ['email']
        widgets = {
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your email'
            })
        }
