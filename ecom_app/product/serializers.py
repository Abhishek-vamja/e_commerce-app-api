"""
Serializer for product view.
"""

from rest_framework import serializers
from rest_framework.response import Response

from core.models import *


class CategorySerializer(serializers.ModelSerializer):
    """Serializer for category."""

    class Meta:
        model = Category
        fields = ['title']


class ProductSerializer(serializers.ModelSerializer):
    """Serializer for product."""

    class Meta:
        model = Product
        fields = [
            'id','title','category','price','description','slug','image','available','date_created'
            ]
    
    def create(self, validated_data):
        product = Product.objects.create(**validated_data)
        
        return product
    
    def update(self, instance, validated_data):
        for attr,value in validated_data.items():
            setattr(instance,attr,value)
        
        instance.save()

        return instance
    

class FavoriteSerializer(serializers.ModelSerializer):
    """Serializer for favorite product objects."""

    class Meta:
        model = Favorite
        fields = ['id','product','status','date_created']


class AddressSerializer(serializers.ModelSerializer):
    """Serializer for address objects."""

    class Meta:
        model = Address
        fields = ['id','slug','address']


class CheckoutSerializer(serializers.ModelSerializer):
    """Serializer for checkout objects."""

    class Meta:
        model = Checkout
        fields = ['id','cart','status','date_checkout']
