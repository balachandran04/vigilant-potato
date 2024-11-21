from django.contrib import admin
from .models import Product, Cart, CartItem, Order, OrderItem, Address, Wishlist,Category

# Admin interface for the Product model
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'stock', 'description')
    search_fields = ('name',)
    list_filter = ('price', 'stock')

admin.site.register(Product, ProductAdmin)

admin.site.register(Category    )
# Admin interface for the CartItem model
class CartItemAdmin(admin.TabularInline):
    model = CartItem
    extra = 1
    fields = ('product', 'quantity')
    readonly_fields = ('total_price',)

# Admin interface for the Cart model
class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'get_total_price')
    inlines = [CartItemAdmin]

    # Define a method to get the total price in the CartAdmin
    def get_total_price(self, obj):
        return obj.total_price()  # Call the total_price method of Cart model
    get_total_price.short_description = 'Total Price'

admin.site.register(Cart, CartAdmin)


# Admin interface for the Address model
class AddressAdmin(admin.ModelAdmin):
    list_display = ('user', 'street_address', 'city', 'country')
    search_fields = ('user', 'city', 'country')

admin.site.register(Address, AddressAdmin)


# Admin interface for the OrderItem model
class OrderItemAdmin(admin.TabularInline):
    model = OrderItem
    extra = 1
    fields = ('product', 'quantity', 'total_price')
    readonly_fields = ('total_price',)

# Admin interface for the Order model
class OrderAdmin(admin.ModelAdmin):
    list_display = ('user', 'shipping_address', 'total_price', 'order_date', 'status')
    list_filter = ('status', 'order_date')
    inlines = [OrderItemAdmin]

admin.site.register(Order, OrderAdmin)


# Admin interface for the Wishlist model
class WishlistAdmin(admin.ModelAdmin):
    list_display = ('user', 'get_product_names')

    # Function to display product names in a comma-separated list
    def get_product_names(self, obj):
        return ", ".join([item.product.name for item in obj.items.all()])
    get_product_names.short_description = 'Wishlist Items'

admin.site.register(Wishlist, WishlistAdmin)
