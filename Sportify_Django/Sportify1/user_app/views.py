from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, UserUpdateForm, AddressForm
from .models import Address

def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        # Get username from email
        try:
            user = User.objects.get(email=email)
            username = user.username
            user = authenticate(request, username=username, password=password)
            
            if user is not None:
                login(request, user)
                # Get the next parameter or default to index
                next_url = request.POST.get('next', 'index')
                return redirect(next_url)
            else:
                messages.error(request, 'Invalid credentials')
        except User.DoesNotExist:
            messages.error(request, 'User with this email does not exist')
    
    # If GET request or authentication failed, redirect to home
    return redirect('index')


def register_view(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone_number = request.POST.get('phone_number')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        
        # Validate passwords match
        if password1 != password2:
            messages.error(request, 'Passwords do not match')
            return redirect('index')
        
        # Check if email already exists
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already registered')
            return redirect('index')
        
        username = email
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password1
        )
        user.first_name = name
        user.save()
        Address.objects.create(user=user, house_street="", pincode="", state="")

        messages.success(request, 'Registration successful! Please log in.')

    return redirect('index')

@login_required
def user_logout(request):
    logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('index')


@login_required
def profile(request):
    if request.method == 'POST':
        if 'update_user' in request.POST:
            u_form = UserUpdateForm(request.POST, instance=request.user)
            a_form = AddressForm(instance=Address.objects.filter(user=request.user).first())
            if u_form.is_valid():
                u_form.save()
                messages.success(request, 'Your personal information has been updated!')
                return redirect('profile')
            else:
                for field, errors in u_form.errors.items():
                    for error in errors:
                        messages.error(request, f"{field}: {error}")
        
        elif 'update_address' in request.POST:
            u_form = UserUpdateForm(instance=request.user)
            address_instance = Address.objects.filter(user=request.user).first()
            a_form = AddressForm(request.POST, instance=address_instance)
            if a_form.is_valid():
                address = a_form.save(commit=False)
                if not address_instance:
                    address.user = request.user
                address.save()
                messages.success(request, 'Your address has been updated!')
                return redirect('index')
            else:
                for field, errors in a_form.errors.items():
                    for error in errors:
                        messages.error(request, f"{field}: {error}")
    else:
        u_form = UserUpdateForm(instance=request.user)
        address_instance = Address.objects.filter(user=request.user).first()
        a_form = AddressForm(instance=address_instance)

    context = {
        'u_form': u_form,
        'a_form': a_form
    }
    return render(request, 'user_app/profile.html', context)


def index(request):
    # Your existing index view code
    # ...
    
    # Add user profile data if user is authenticated
    user_profile = None
    if request.user.is_authenticated:
        try:
            user_profile = {
                'username': request.user.username,
                'name': request.user.first_name or request.user.username,
                'email': request.user.email,
                'date_joined': request.user.date_joined,
                'address': request.user.address if hasattr(request.user, 'address') else None
            }
        except:
            pass
    
    context = {
        # Your existing context
        # ...
        'user_profile': user_profile,
    }
    
    return render(request, 'index.html', context)

