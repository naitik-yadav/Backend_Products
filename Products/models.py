from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone
from utils.base_models import CreatedUpdatedOnMixin, RequestResponseMixin
  

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('role', 'admin')

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)

class CustomUser(CreatedUpdatedOnMixin, RequestResponseMixin, AbstractBaseUser, PermissionsMixin):
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('user', 'User'),
    ]
    
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    contact_number = models.CharField(max_length=15, blank=True, null=True, unique=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='user')
    profile_photo = models.ImageField(upload_to='profile_photos/', blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    
    objects = CustomUserManager()
    
    USERNAME_FIELD = 'email' 
    REQUIRED_FIELDS = ['first_name', 'last_name']

    def __str__(self):
        return self.email 
    
    @property
    def is_admin(self):
        return self.role == 'admin'
    
    @property
    def is_user(self):
        return self.role == 'user'      


class Products(CreatedUpdatedOnMixin, RequestResponseMixin):
    product_name = models.CharField(max_length=80)
    product_number = models.IntegerField()
    product_type = models.CharField(max_length=225)
    description = models.CharField(max_length=225)
    category = models.CharField(max_length=225)
    Price = models.DecimalField(max_digits=10, decimal_places=2)
    images = models.ImageField(upload_to='products/', blank=True, null=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)


class Cart(CreatedUpdatedOnMixin, RequestResponseMixin):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='cart')

    def __str__(self):
        return f"Cart for {self.user.email}"

class CartItem(CreatedUpdatedOnMixin, RequestResponseMixin):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.product.product_name} x {self.quantity} in {self.cart}"

class Order(CreatedUpdatedOnMixin, RequestResponseMixin):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='orders')
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='order')
    order_status = models.CharField(max_length=20, choices=[
        ('pending', 'Pending'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled')
    ], default='pending')

    def __str__(self):
        return f"Order for {self.user.email} - {self.order_status}"

class OrderItem(CreatedUpdatedOnMixin, RequestResponseMixin):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.product.product_name} x {self.quantity} in {self.order}"