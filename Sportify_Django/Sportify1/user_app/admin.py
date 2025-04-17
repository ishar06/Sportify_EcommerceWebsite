from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import Address

class AddressInline(admin.StackedInline):
    model = Address
    can_delete = True
    verbose_name_plural = 'Address'

class UserAdmin(BaseUserAdmin):
    inlines = (AddressInline,)
    list_display = ('username', 'email', 'first_name', 'is_staff')

# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
