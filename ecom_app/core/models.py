"""
Models for our API.
"""

from typing import Any
from django.db import models
from django.conf import settings
from django.contrib.auth.models import (
    AbstractBaseUser , PermissionsMixin , BaseUserManager
    )


# ...Model for user app

class UserManager(BaseUserManager):
    """Manager for user."""

    def create_user(self,email,password=None,**extra_fields):
        """Create,save and return new user."""

        if not email:
            raise ValueError('User must have an email address.')
        
        user = self.model(email=self.normalize_email(email),**extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user
    
    def create_superuser(self,email,password):
        """Create and return a new superuser"""
        user = self.create_user(email,password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user
    

class User(AbstractBaseUser,PermissionsMixin):
    """User in the system."""
    email = models.EmailField(max_length=255,unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'


# ...Models for product app

class Category(models.Model):
    """Categories for many products."""
    title = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Categorie"

    def __str__(self):
        return self.title


class Product(models.Model):
    """Product objects."""   
    title = models.CharField(max_length=255)
    category = models.ForeignKey(Category,related_name="product",on_delete=models.CASCADE)
    price = models.FloatField()
    description = models.TextField()
    image = models.ImageField(upload_to='img/prod',null=True)
    available = models.BooleanField(default=True)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '{}, {}'.format(self.title,self.category)

class Address(models.Model):
    """Address of users objects."""
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    address = models.TextField()

    def __str__(self):
        return self.user

class Cart(models.Model):
    """Cart objects."""
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    product = models.ManyToManyField(Product)
    address = models.ForeignKey(Address,on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date_created']

    def __str__(self):
        return self.user


STATUS_CHOICE = (
    ('Order Pending','Order Pending'),
    ('Confirmed','Confirmed'),
    ('Packed','Packed'),
    ('Shipped','Shipped'),
    ('Outer Delivery','Outer Delivery'),
    ('Delivered','Delivered'),
    ('Favorite','Favorite')
)

class Favorite(models.Model):
    """Favorite products objects."""
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    Product = models.ForeignKey(Product,on_delete=models.CASCADE)
    status = models.CharField(max_length=255,choices=STATUS_CHOICE,default='Favorite')
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user

class CheckOut(models.Model):
    """Checkout product objects."""
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    cart = models.ManyToManyField(Cart)
    status = models.CharField(max_length=255,choices=STATUS_CHOICE,default='Confirmed')
    date_checkout = models.DateField(auto_now_add=True)
    date_delivered = models.DateField()

    def __str__(self):
        return self.user