"""
View for product API's.
"""

from rest_framework import viewsets

from core.models import Category,Product
from .serializers import *

from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import filters , mixins
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated , IsAdminUser


class ProductView(viewsets.ReadOnlyModelViewSet):
    """Handle product view."""

    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    # ...filter system

    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['category','title']

    # ...For search fields in project.
    
    # filter_backends = [filters.SearchFilter]
    # search_fields = ('title',)


class ProductDetail(mixins.CreateModelMixin,
                    mixins.DestroyModelMixin,
                    mixins.UpdateModelMixin,
                    mixins.ListModelMixin,
                    viewsets.GenericViewSet):
    """Handle products objects create , update and delete.
    This class accessible only for Admin.
    """

    serializer_class = ProductSerializer
    queryset = Product.objects.all()

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated,IsAdminUser]

    filter_backends = [filters.SearchFilter]
    search_fields = ('title',)