"""
Serializer for product view.
"""

from rest_framework import serializers

from core.models import Category , Product


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
            'id','title','category','price','description','image','available','date_created'
            ]
    
    def create(self, validated_data):
        product = Product.objects.create(**validated_data)
        
        return product
    
    def update(self, instance, validated_data):
        for attr,value in validated_data.items():
            setattr(instance,attr,value)
        
        instance.save()

        return instance
