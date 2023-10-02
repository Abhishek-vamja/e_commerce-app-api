"""
Serializer for product view.
"""

from rest_framework import serializers
from rest_framework.fields import empty
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
            'id','title','price','image'
            ]
    
    def create(self, validated_data):
        product = Product.objects.create(**validated_data)
        
        return product
    
    def update(self, instance, validated_data):
        for attr,value in validated_data.items():
            setattr(instance,attr,value)
        
        instance.save()

        return instance
    
class ProductDetailSerializer(serializers.ModelSerializer):
    """Serializer for detail product view."""

    class Meta:
        model = Product
        fields = ['id','image','title','price','description','available']

class FavoriteSerializer(serializers.ModelSerializer):
    """Serializer for favorite product objects."""

    class Meta:
        model = Favorite
        fields = ['id','product','status','date_created']

class FavoriteDetailSerializer(serializers.ModelSerializer):
    """Serializer for favorite objects details."""

    class Meta:
        model = Favorite
        fields = ['id','product','status']

    def __init__(self, *args, **kwargs):
        super(FavoriteDetailSerializer,self).__init__(*args,**kwargs)
        self.Meta.depth = 1

class CartSerializer(serializers.ModelSerializer):
    """Serializer for cart objects."""

    class Meta:
        model = Cart
        fields = ['id','product','quantity','date_created']


class CheckoutSerializer(serializers.ModelSerializer):
    """Serializer for checkout objects."""

    class Meta:
        model = Checkout
        fields = ['id','full_name','phone','email','address','note']


class OrderSerializer(serializers.ModelSerializer):
    """Serializer for order objects."""
    items = serializers.PrimaryKeyRelatedField(many=True,queryset=Product.objects.all())

    class Meta:
        model = OrderPlaced
        fields = ['id','items','status','paid','payment','ordered_date']
    
    def create(self, validated_data):
        items_data =validated_data.pop('items')
        order = OrderPlaced.objects.create(**validated_data)

        for item_data in items_data:
            order.items.add(item_data)
        return order

