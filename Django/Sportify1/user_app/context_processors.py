from .models import Address

def user_address(request):
    address = None
    if request.user.is_authenticated:
        try:
            address = Address.objects.get(user=request.user)
        except Address.DoesNotExist:
            pass
    return {'address': address}
