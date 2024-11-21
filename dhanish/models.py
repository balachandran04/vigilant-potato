from django.db import models
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.validators import MinValueValidator

# Category Model to classify products
class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    slug = models.SlugField(unique=True)
    image = models.ImageField(upload_to='category_images/', default='category_images/default.jpg')
    def __str__(self):
        return self.name


# Product Model
class Product(models.Model):
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    image = models.ImageField(upload_to='product_images/')
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.BooleanField(default=False, help_text='0-show, 1-Hidden')
    trending = models.BooleanField(default=False, help_text='0-default, 1-Trending')
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name

    def is_in_stock(self):
        return self.stock > 0

    def reduce_stock(self, quantity):
        if self.stock >= quantity:
            self.stock -= quantity
            self.save()

    def increase_stock(self, quantity):
        self.stock += quantity
        self.save()


# Address Model
class Address(models.Model):
    user = models.ForeignKey(User, related_name="addresses", on_delete=models.CASCADE)
    street_address = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    country = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.street_address}, {self.city}, {self.country}"


# Cart Model to store the user's shopping cart
class Cart(models.Model):
    user = models.OneToOneField(User, related_name='cart', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Cart of {self.user.username}"


# CartItem Model to store items in the user's cart
class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='cart_items', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.quantity} of {self.product.name}"

    def total_price(self):
        return self.quantity * self.product.price


# Order Model with Cash on Delivery (COD) Option
class Order(models.Model):
    user = models.ForeignKey(User, related_name="orders", on_delete=models.CASCADE)
    order_date = models.DateTimeField(auto_now_add=True)
    shipping_address = models.ForeignKey(Address, related_name="orders", on_delete=models.SET_NULL, null=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    status = models.CharField(
        max_length=20,
        choices=[('Pending', 'Pending'), ('Shipped', 'Shipped'), ('Delivered', 'Delivered')],
        default='Pending'
    )
    payment_method = models.CharField(
        max_length=20,
        choices=[('COD', 'Cash on Delivery'), ('Online', 'Online Payment')],
        default='COD'
    )
    payment_status = models.CharField(
        max_length=20,
        choices=[('Pending', 'Pending'), ('Completed', 'Completed'), ('Failed', 'Failed')],
        default='Pending'
    )

    def __str__(self):
        return f"Order #{self.id} for {self.user.username}"

    def calculate_total(self):
        total = sum(item.total_price() for item in self.items.all())
        self.total_price = total
        self.save()

    def mark_as_paid(self):
        if self.payment_method == 'COD':
            # COD payments are completed when the order is delivered
            self.payment_status = 'Pending'  # COD is pending until delivery
        else:
            self.payment_status = 'Completed'
        self.save()


# OrderItem Model to store products in an order
class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='order_items', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price_at_time_of_order = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return f"{self.quantity} of {self.product.name} in Order #{self.order.id}"

    def total_price(self):
        # Check if price_at_time_of_order is None and handle accordingly
        if self.price_at_time_of_order is None:
            return 0  # or return some default value, like 0.0 or log the error
        return self.quantity * self.price_at_time_of_order


# Wishlist Model to store user's wishlist
class Wishlist(models.Model):
    user = models.ForeignKey(User, related_name="wishlist", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Wishlist of {self.user.username}"


# WishlistItem Model to store items in the user's wishlist
class WishlistItem(models.Model):
    wishlist = models.ForeignKey(Wishlist, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='wishlist_items', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.product.name} in {self.wishlist.user.username}'s Wishlist"


# Payment Model (COD and other methods)
class Payment(models.Model):
    order = models.ForeignKey(Order, related_name="payments", on_delete=models.CASCADE)
    payment_date = models.DateTimeField(auto_now_add=True)
    payment_method = models.CharField(max_length=50)
    payment_status = models.CharField(
        max_length=50,
        choices=[('Pending', 'Pending'), ('Completed', 'Completed'), ('Failed', 'Failed')],
        default='Pending'
    )
    payment_amount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Payment for Order #{self.order.id} - {self.payment_status}"
