from .models import Address

def user_address(request):
    """
    Context processor to add user address and auth info to all templates
    """
    context = {}
    
    # Check both Django authentication and Flask token
    if request.user.is_authenticated and request.session.get('user_token'):
        try:
            # Use filter instead of get to avoid errors if multiple addresses exist
            addresses = Address.objects.filter(user=request.user)
            if addresses.exists():
                context['user_address'] = addresses.first()
                context['user_addresses'] = addresses
            
            # Add user info from Flask session
            context['user_name'] = request.session.get('user_name')
            context['user_token'] = request.session.get('user_token')
            
        except Exception as e:
            print(f"Error in user_address context processor: {e}")
            context['user_address'] = None
            context['user_addresses'] = []
    
    return context

from cart_app.models import Category, CartItem

def user_context(request):
    """
    Context processor to add user-related data to all templates
    """
    context = {}
    
    # Add categories to context for all templates
    categories = Category.objects.all()
    context['categories'] = categories
    
    if request.user.is_authenticated:
        # Add user addresses to context
        from user_app.models import Address
        user_addresses = Address.objects.filter(user=request.user)
        
        # Add cart count to context
        cart_count = CartItem.objects.filter(user=request.user).count()
        
        context.update({
            'user_addresses': user_addresses,
            'cart_count': cart_count,
        })
    
    return context
