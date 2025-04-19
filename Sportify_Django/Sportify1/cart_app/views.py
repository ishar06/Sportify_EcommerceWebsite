from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q, F
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import Category, Product, CartItem, Order, OrderItem, Subscription
from user_app.models import Address
from .forms import CheckoutForm, SubscriptionForm


def index(request):
    categories = Category.objects.all()
    featured_products = Product.objects.all().order_by('?')[:8]
    return render(request, 'cart_app/index.html', {
        'categories': categories,
        'featured_products': featured_products
    })

def product_list(request, category_slug=None):
    category = get_object_or_404(Category, slug=category_slug) if category_slug else None
    products = Product.objects.filter(category=category) if category else Product.objects.all()
    
    # Price Range Filter
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    if min_price:
        products = products.filter(price__gte=float(min_price))
    if max_price:
        products = products.filter(price__lte=float(max_price))
    
    # Stock Filter
    stock_status = request.GET.get('stock_status')
    if stock_status == 'in_stock':
        products = products.filter(stock__gt=0)
    elif stock_status == 'out_of_stock':
        products = products.filter(stock=0)
    
    # Rating Filter
    min_rating = request.GET.get('min_rating')
    if min_rating:
        products = products.filter(rating__gte=float(min_rating))
    
    # Sorting
    sort = request.GET.get('sort')
    if sort:
        if sort == 'price_asc':
            products = products.order_by('price')
        elif sort == 'price_desc':
            products = products.order_by('-price')
        elif sort == 'rating_desc':
            products = products.order_by('-rating')
    
    context = {
        'category': category,
        'products': products,
    }
    return render(request, 'cart_app/product_list.html', context)


def search(request):
    query = request.GET.get('query', '')
    products = Product.objects.filter(
        Q(title__icontains=query) | Q(description__icontains=query)
    )
    return render(request, 'cart_app/search_results.html', {
        'query': query,
        'products': products
    })

@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    
    # Check if product is in stock
    if product.stock <= 0:
        messages.error(request, f"Sorry, {product.title} is out of stock.")
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', reverse('index')))
    
    # Check if product already in cart
    cart_item, created = CartItem.objects.get_or_create(
        user=request.user,
        product=product,
        defaults={'quantity': 1}
    )
    
    if not created:
        # Check if adding one more would exceed stock
        if cart_item.quantity >= product.stock:
            messages.warning(request, f"Sorry, we only have {product.stock} of {product.title} in stock.")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', reverse('index')))
        
        cart_item.quantity += 1
        cart_item.save()
    
    messages.success(request, f"{product.title} added to cart!")
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', reverse('index')))


@login_required
def cart(request):
    cart_items = CartItem.objects.filter(user=request.user)
    total = sum(item.get_total_price() for item in cart_items)

    return render(request, 'cart_app/cart.html', {
        'cart_items': cart_items,
        'total': total
    })


@login_required
def update_cart(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id, user=request.user)
    action = request.POST.get('action')
    
    if action == 'increase':
        # Check if increasing would exceed stock
        if cart_item.quantity >= cart_item.product.stock:
            messages.warning(request, f"Sorry, we only have {cart_item.product.stock} of {cart_item.product.title} in stock.")
        else:
            cart_item.quantity += 1
            cart_item.save()
    elif action == 'decrease':
        cart_item.quantity -= 1
        if cart_item.quantity <= 0:
            cart_item.delete()
        else:
            cart_item.save()
    elif action == 'remove':
        cart_item.delete()
    
    return redirect('cart')

@login_required
def checkout(request):
    cart_items = CartItem.objects.filter(user=request.user)
    
    if not cart_items:
        messages.error(request, 'Your cart is empty!')
        return redirect('cart')

    # Check if any item exceeds stock
    for item in cart_items:
        if item.quantity > item.product.stock:
            messages.error(request, f"Sorry, we only have {item.product.stock} of {item.product.title} in stock.")
            return redirect('cart')
    
    try:
        address = Address.objects.get(user=request.user)
    except Address.DoesNotExist:
        messages.warning(request, 'Please add a shipping address before checkout!')
        address = None
    
    total = sum(item.get_total_price() for item in cart_items)
    
    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            payment_method = form.cleaned_data['payment_method']
            
            # Create order
            order = Order.objects.create(
                user=request.user,
                total_amount=total,
                payment_method=payment_method,
                shipping_address=address.get_full_address()
            )
            
            # Create order items and update stock
            for cart_item in cart_items:
                OrderItem.objects.create(
                    order=order,
                    product_name=cart_item.product.title,
                    product_price=cart_item.product.price,
                    quantity=cart_item.quantity,
                    image_url=cart_item.product.image.url
                )
                
                # Update product stock
                product = cart_item.product
                product.stock -= cart_item.quantity
                product.save()
            
            # Clear cart
            cart_items.delete()
            
            messages.success(request, 'Order placed successfully!')
            return redirect('order_history')
        else:
            for error in form.non_field_errors():
                messages.error(request, error)
    else:
        form = CheckoutForm()
    
    return render(request, 'cart_app/checkout.html', {
        'cart_items': cart_items,
        'total': total,
        'address': address,
        'form': form
    })

@login_required
def order_history(request):
    orders = Order.objects.filter(user=request.user).order_by('-order_date')
    return render(request, 'cart_app/orders.html', {'orders': orders})

def about(request):
    return render(request, 'cart_app/about.html')

def terms_conditions(request):
    return render(request, 'cart_app/tc.html')

def privacy_policy(request):
    return render(request, 'cart_app/privacy_policy.html')

def exchange_policy(request):
    return render(request, 'cart_app/exchange_policy.html')

def blogs(request):
    return render(request, 'cart_app/blogs.html')

def csr(request):
    return render(request, 'cart_app/csr.html')

from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse



def subscribe(request):
    if not request.user.is_authenticated:
        messages.error(request, 'You need to be logged in to subscribe.')
        return redirect('index')

    if request.method == 'POST':
        form = SubscriptionForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            if Subscription.objects.filter(email=email).exists():
                messages.info(request, 'You are already subscribed to our newsletter!')
            else:
                Subscription.objects.create(email=email)
                messages.success(request, 'Subscription successful! Check your email for future updates.')
        else:
            messages.error(request, 'Please enter a valid email address | User already exists')
    
    return redirect(request.META.get('HTTP_REFERER', 'index'))