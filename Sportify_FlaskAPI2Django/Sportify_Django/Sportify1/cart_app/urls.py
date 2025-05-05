from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('search/', views.search, name='search'),
    path('category/<slug:category_slug>/', views.product_list, name='product_list'),
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.cart, name='cart'),
    path('update-cart/<int:item_id>/', views.update_cart, name='update_cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('orders/', views.order_history, name='order_history'),
    path('about/', views.about, name='about'),
    path('terms-conditions/', views.terms_conditions, name='tc'),
    path('privacy-policy/', views.privacy_policy, name='privacy_policy'),
    path('exchange-policy/', views.exchange_policy, name='exchange_policy'),
    path('blogs/', views.blogs, name='blogs'),
    path('csr/', views.csr, name='csr'),
    path('subscribe/', views.subscribe, name='subscribe'),
]
