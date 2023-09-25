"""
View for product API's.
"""

from core.models import *
from .serializers import *

from http import HTTPStatus

from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.pagination import PageNumberPagination
from rest_framework import filters , mixins
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated , IsAdminUser


class LargeResultsSetPagination(PageNumberPagination):
    """Modify pagination style."""
    page_size = 3
    page_size_query_param = 'page_size'
    max_page_size = 10000


class product(viewsets.ReadOnlyModelViewSet):
    """Show all products."""
    serializer_class = ProductSerializer
    queryset = Product.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    # ...Filter
    #  filter_backends = [DjangoFilterBackend]
    #  filterset_fields = ['category','title']

    """Search field."""
    filter_backends = [filters.SearchFilter]
    search_fields = ('title','slug')

    """Pagination."""
    pagination_class = LargeResultsSetPagination


class Product_detail_for_admin(
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    mixins.UpdateModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet
    ):
    """Handle products objects create , update and delete.
    This class accessible only for Admin.
    """
    serializer_class = ProductSerializer
    queryset = Product.objects.all()

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated,IsAdminUser]

    filter_backends = [filters.SearchFilter]
    search_fields = ('title','slug')

    pagination_class = LargeResultsSetPagination


class AddressView(viewsets.ModelViewSet):
    """Handle address of authenticated user."""

    serializer_class = AddressSerializer
    queryset = Address.objects.all()

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    pagination_class = None

    def get_queryset(self):
        """Get objects for authenticated users."""
        queryset = self.queryset
        return queryset.filter(user=self.request.user).order_by('-id').distinct()
    

class FavoriteView(viewsets.ReadOnlyModelViewSet):
    """Handle favorite product objects create , update and delete."""
    serializer_class = FavoriteSerializer
    queryset = Favorite.objects.all()

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    pagination_class = LargeResultsSetPagination

    def get_queryset(self):
        """Get object for authenticated users."""
        queryset = self.queryset
        return queryset.filter(user=self.request.user).order_by('-id').distinct()


class Create_favorite(APIView):
    """Handle create , update and delete favorite objects."""

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self,request: Request,product_id: str) -> Response:
        try:
            Favorite.objects.get(user_id=str(request.user.id),product_id=str(Product.objects.get(id=product_id).id))
            return Response({'msg':'Already added in favorite items!!','url':'http://127.0.0.1:8000/api/product/favorite/my/'},status=HTTPStatus.OK)
        except:
            Favorite.objects.create(user_id=str(request.user.id),product_id=str(Product.objects.get(id=product_id).id))
            return Response({'msg':'Added to favorite items!!','url':'http://127.0.0.1:8000/api/product/favorite/my/'},status=HTTPStatus.OK)


class checkout(viewsets.ReadOnlyModelViewSet):
    """List checkout objects."""

    serializer_class = CheckoutSerializer
    queryset = Checkout.objects.all()

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    pagination_class = None

    def get_queryset(self):
        """Get objects for authenticated users."""
        queryset = self.queryset
        return queryset.filter(user=self.request.user).order_by('-id').distinct()


class Create_checkout(APIView):
    """Return new checkout object."""
    pass 