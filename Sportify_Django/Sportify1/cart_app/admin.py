from django.contrib import admin
from .models import Category, Product, CartItem, Order, OrderItem, Subscription

class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'price', 'stock', 'is_in_stock')
    list_filter = ('category', 'stock')
    search_fields = ('title', 'description')
    list_editable = ('stock','price',)
    
    def is_in_stock(self, obj):
        return obj.stock > 0
    is_in_stock.boolean = True
    is_in_stock.short_description = 'In Stock'

class CartItemAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'quantity')
    list_filter = ('user',)
    search_fields = ('user__username', 'product__title')

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ('product_name', 'product_price', 'quantity', 'image_url')

class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'total_amount', 'status', 'payment_method', 'order_date')
    list_filter = ('status', 'payment_method', 'order_date')
    search_fields = ('user__username', 'user__email')
    inlines = [OrderItemInline]
    readonly_fields = ('user', 'total_amount', 'payment_method', 'shipping_address', 'order_date')

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}

class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('email', 'date_subscribed')
    search_fields = ('email',)
    readonly_fields = ('date_subscribed',)

admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(CartItem, CartItemAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem)
admin.site.register(Subscription, SubscriptionAdmin)
