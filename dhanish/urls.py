from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name='home'),  # Home page displaying products
    path('register/', views.register, name='register'),  # Register a new user
    path('login/', views.user_login, name='login'),  # Login page
    path('logout/', views.user_logout, name='logout'),  # Logout user
    path('cart/', views.view_cart, name='cart'),  # View the shopping cart
    path('add_to_cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),  # Add to cart
    path('remove_from_cart/<int:cart_item_id>/', views.remove_from_cart, name='remove_from_cart'),  # Remove from cart
    path('checkout/', views.checkout, name='checkout'),  # Checkout page
    path('order_summary/<int:order_id>/', views.order_summary, name='order_summary'),  # Order summary after checkout
    path('add_to_wishlist/<int:product_id>/', views.add_to_wishlist, name='add_to_wishlist'),  # Add product to wishlist
    path('wishlist/', views.view_wishlist, name='wishlist'),  # View wishlist
    path('remove_from_wishlist/<int:wishlist_item_id>/', views.remove_from_wishlist, name='remove_from_wishlist'),  # Remove from wishlist
    path('add_address/', views.add_address, name='add_address'),  
    path('product_details/<int:id>/', views.product_details, name='product_details'),
    path('order/<int:order_id>/status/', views.order_status, name='order_status')
# Add new address for user
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)