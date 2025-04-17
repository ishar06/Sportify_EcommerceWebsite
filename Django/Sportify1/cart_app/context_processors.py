from .models import CartItem, Category, Product
import random

def cart_count(request):
    count = 0
    if request.user.is_authenticated:
        count = CartItem.objects.filter(user=request.user).count()
    return {'cart_count': count}

def categories_processor(request):
    categories = Category.objects.all()
    return {'categories': categories}

def featured_products(request):
    # Get 8 random products for the featured section
    featured = list(Product.objects.all().order_by('?')[:8])
    return {'featured_products': featured}
