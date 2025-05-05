import requests
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import login as auth_login, authenticate, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .forms import UserRegisterForm, UserUpdateForm, AddressForm
from .models import Address

# Flask API URL (Change this to your actual Flask server URL)
FLASK_API_URL = "http://localhost:5000/api"  # Update this with your Flask server URL





def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        # Try to get user by email
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            messages.error(request, 'Invalid email or password.')
            return JsonResponse({
                'status': 'error',
                'message': 'Invalid email or password'
            }, status=400)

        # Authenticate user
        user = authenticate(username=user.username, password=password)
        if user is not None:
            auth_login(request, user)
            # Set user token in session
            request.session['user_token'] = f"user_token_{user.id}"  # Simple token generation
            return JsonResponse({
                'status': 'success',
                'message': 'Login successful'
            })
        else:
            messages.error(request, 'Invalid email or password.')
            return JsonResponse({
                'status': 'error',
                'message': 'Invalid email or password'
            }, status=400)
    
    return redirect('index')


def register_view(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone_number = request.POST.get('phoneNumber')
        password = request.POST.get('password')
        
        # Check if email already exists
        if User.objects.filter(email=email).exists():
            return JsonResponse({
                'status': 'error',
                'message': 'Email already registered'
            }, status=400)
        
        try:
            # Create Django user with proper password
            user = User.objects.create_user(
                username=email,
                email=email,
                password=password,  # This will properly hash the password
                first_name=name
            )
            
            # Store additional user data in session
            request.session['user_phone'] = phone_number
            # Set user token in session
            request.session['user_token'] = f"user_token_{user.id}"
            
            return JsonResponse({
                'status': 'success',
                'message': 'Registration successful! Please log in.'
            })
        except Exception as e:
            return JsonResponse({
                'status': 'error',
                'message': str(e)
            }, status=400)
    
    return redirect('index')


@login_required
def user_logout(request):
    # Clear session to log out user
    logout(request)
    request.session.flush()
    messages.info(request, 'You have been logged out.')
    return redirect('index')


# def login_view(request):
#     if request.method == 'POST':
#         email = request.POST.get('email')
#         password = request.POST.get('password')
        
#         # Get auth token from request session
#         auth_token = request.session.get('user_token')
        
#         # Send POST request to Flask API for login
#         response = requests.post('http://127.0.0.1:5000/login', json={
#             'email': email,
#             'password': password
#         })

#         if response.status_code == 200:
#             data = response.json()
            
#             # Store token and user info in session
#             request.session['user_token'] = data.get('token')
#             request.session['user_name'] = data.get('user', {}).get('name')
#             request.session['user_email'] = email
            
#             # Store authentication state in session
#             request.session['is_authenticated'] = True
            
#             # Create or get Django user
#             if not User.objects.filter(username=email).exists():
#                 User.objects.create_user(username=email, email=email)
            
#             # Return success response
#             return JsonResponse({
#                 'status': 'success',
#                 'token': data.get('token'),
#                 'user': {
#                     'name': data.get('user', {}).get('name'),
#                     'email': email
#                 }
#             })
#         else:
#             # Return error response
#             return JsonResponse({
#                 'status': 'error',
#                 'message': response.json().get('message', 'Login failed')
#             }, status=response.status_code)
    
#     return redirect('index')


# def register_view(request):
#     if request.method == 'POST':
#         name = request.POST.get('name')
#         email = request.POST.get('email')
#         phone_number = request.POST.get('phoneNumber')
#         password = request.POST.get('password')
        
#         # Check if email already exists
#         if User.objects.filter(email=email).exists():
#             return JsonResponse({
#                 'status': 'error',
#                 'message': 'Email already registered'
#             }, status=400)
        
#         # Sending POST request to Flask API for registration
#         payload = {
#             'name': name,
#             'email': email,
#             'phoneNumber': phone_number,
#             'password': password
#         }
        
#         response = requests.post('http://127.0.0.1:5000/signup', json=payload)
        
#         if response.status_code == 201:
#             # Create Django user
#             User.objects.create_user(
#                 username=email,
#                 email=email,
#                 first_name=name
#             )
            
#             return JsonResponse({
#                 'status': 'success',
#                 'message': 'Registration successful! Please log in.'
#             })
#         else:
#             error_message = response.json().get('message', 'Registration failed.')
#             return JsonResponse({
#                 'status': 'error',
#                 'message': error_message
#             }, status=response.status_code)
    
#     return redirect('index')


# @login_required
# def user_logout(request):
#     # Clear session to log out user
#     request.session.flush()
#     messages.info(request, 'You have been logged out.')
#     return redirect('index')


@login_required
def profile(request):
    # Get user's addresses
    addresses = Address.objects.filter(user=request.user)
    
    context = {
        'user': request.user,
        'addresses': addresses,
    }
    return render(request, 'user_app/profile.html', context)


@login_required
def cart(request):
    return render(request, 'cart_app/cart.html')


@login_required
def address_list(request):
    addresses = Address.objects.filter(user=request.user)
    return render(request, 'user_app/address_list.html', {'addresses': addresses})


@login_required
def add_address(request):
    if request.method == 'POST':
        form = AddressForm(request.POST)
        if form.is_valid():
            address = form.save(commit=False)
            address.user = request.user
            address.save()
            messages.success(request, 'Address added successfully!')
            
            # If this is an AJAX request, return JSON response
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'success': True})
            return redirect('address_list')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    else:
        form = AddressForm()
    
    context = {'form': form, 'action': 'Add'}
    
    # If this is an AJAX request, return the form HTML
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return render(request, 'user_app/address_form_modal.html', context)
    
    return render(request, 'user_app/address_form.html', context)


@login_required
def edit_address(request, address_id):
    address = get_object_or_404(Address, id=address_id, user=request.user)
    
    if request.method == 'POST':
        form = AddressForm(request.POST, instance=address)
        if form.is_valid():
            form.save()
            messages.success(request, 'Address updated successfully!')
            
            # If this is an AJAX request, return JSON response
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'success': True})
            return redirect('address_list')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    else:
        form = AddressForm(instance=address)
    
    context = {'form': form, 'action': 'Edit', 'address': address}
    
    # If this is an AJAX request, return the form HTML
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return render(request, 'user_app/address_form_modal.html', context)
    
    return render(request, 'user_app/address_form.html', context)


@login_required
def delete_address(request, address_id):
    address = get_object_or_404(Address, id=address_id, user=request.user)
    
    # Don't allow deleting the only address
    if Address.objects.filter(user=request.user).count() <= 1:
        messages.error(request, 'You must have at least one address!')
        return redirect('address_list')
    
    address.delete()
    messages.success(request, 'Address deleted successfully!')
    return redirect('address_list')


@login_required
def set_default_address(request, address_id):
    address = get_object_or_404(Address, id=address_id, user=request.user)

    # Reset all addresses to non-default
    Address.objects.filter(user=request.user).update(is_default=False)

    # Set the selected one as default
    address.is_default = True
    address.save()

    messages.success(request, "Default address updated.")
    return redirect('address_list')


@login_required
def edit_profile(request):
    if request.method == 'POST':
        try:
            # Update Django user
            user = request.user
            user.first_name = request.POST.get('name')
            user.email = request.POST.get('email')
            user.save()
            
            # Update session data
            request.session['user_name'] = user.first_name
            request.session['user_email'] = user.email
            request.session['user_phone'] = request.POST.get('phone_number', '')
            
            messages.success(request, 'Profile updated successfully!')
            return redirect('profile')
        except Exception as e:
            messages.error(request, f'Failed to update profile: {str(e)}')
            return redirect('edit_profile')
    
    # Get current user data from Django
    context = {
        'name': request.user.first_name,
        'email': request.user.email,
        'phone_number': request.session.get('user_phone', '')
    }
    
    return render(request, 'user_app/edit_profile.html', context)
