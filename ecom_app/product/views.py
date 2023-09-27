"""
View for product API's.
"""

from core.models import *
from .serializers import *

from http import HTTPStatus

from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import viewsets
from django.core.exceptions import ObjectDoesNotExist
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


class ProductView(viewsets.ReadOnlyModelViewSet):
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
    

class FavoriteView(viewsets.ReadOnlyModelViewSet):
    """Handle favorite product objects create , update and delete."""
    serializer_class = FavoriteSerializer
    queryset = Favorite.objects.all()

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    pagination_class = LargeResultsSetPagination

    def get_queryset(self):
        """Get objects for authenticated users."""
        queryset = self.queryset
        return queryset.filter(user=self.request.user).order_by('-id').distinct()


class Add_to_favorite(APIView):
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


class CartView(viewsets.ViewSet):
    """
    A simple Viewsets for listing or retrieving cart objects..
    """

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def list(self,request: Request):
        all_cart = Cart.objects.all()
        cart = all_cart.filter(user=request.user).order_by('-id').distinct()
        serializer = CartSerializer(cart,many=True)
        carts = Cart.objects.filter(user=self.request.user)

        """Get total price for all items in carts."""
        amount = 0
        for c in cart:
            value = c.quantity * c.product.price
            amount = amount + value
        total = amount

        my_list = []
        for i in carts:
            my_list.append(str(i.product.title))
        
        if serializer.data == []:
            return Response({'Message':'Your cart is empty!!'})
        
        return Response({'Cart_Items':{'Data':serializer.data,'product_name':my_list,'Total_cart_amount':total}})

class Add_to_cart(APIView):
    """Create cart item objects."""

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self,request: Request, product_id: str) -> Response:
        try:
           cart_obj = Cart.objects.get(user_id=str(request.user.id),product_id=str(Product.objects.get(id=product_id).id))
           if cart_obj:               
                cart_obj.quantity += 1
                cart_obj.save()
                return Response({'Message':'Quantity Updated Successfully!!'},status=HTTPStatus.OK)             
        except:
            Cart.objects.create(user_id=str(request.user.id),product_id=str(Product.objects.get(id=product_id).id))
            return Response({'Message':'Add to cart successfully!!'},status=HTTPStatus.OK)


class CheckoutView(viewsets.ViewSet):
    """
    Listing your checkouts objects.
    """
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def list(self,request: Request) -> Response:
        checkout_obj = Checkout.objects.all()
        checkout = checkout_obj.filter(user=self.request.user).order_by('-id').distinct()
        
        cart_obj = Cart.objects.all()
        cart = cart_obj.filter(user=self.request.user).order_by('-id').distinct()

        carts = Cart.objects.filter(user=self.request.user)
        # print(len(carts),'LENNNN!!!!')

        amount = 0
        for c in cart:
            value = c.quantity * c.product.price
            amount = amount + value
        total_price = amount

        my_list = []
        for i in carts:
            my_list.append(str(i.product))
        # print(my_list)
        
        serializer = CheckoutSerializer(checkout,many=True)

        if serializer.data == []:
            return Response({'Checkout':'Please fill up the data!!','products':my_list,'Total_pay_amount':total_price})
        return Response({'Checkout':{'Data':serializer.data,'products':my_list,'Total_pay_amount':total_price}})
    
    def create(self,request: Request) -> Response:
        checkout_obj = Checkout.objects.all()
        checkout = checkout_obj.filter(user=request.user).order_by('-id').distinct()

        serializer = CheckoutSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save(user=self.request.user)
            return Response(serializer.data)
        
        return Response(serializer.errors)

class Orders(APIView):
    """Listing all order objects for authenticated user."""
    
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self,request: Request) -> Response:
        order_obj = OrderPlaced.objects.all()
        order = order_obj.filter(user=self.request.user).order_by('-id').distinct()

        serializer = OrderSerializer(order,many=True)

        if serializer.data == []:
            return Response({'Message':'Not order yet!!'})
        return Response(serializer.data)

#.. Work on it
class OrderView(APIView):
    """
    Listing and creating order objects for authenticated user.
    """

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self,request: Request, cart_id: str) -> Response:
        try:
            OrderPlaced.objects.create(user_id=str(request.user.id),cart_id=str(Cart.objects.get(id=cart_id).id))
        except Exception as e:
            print(e,'EEEE')
        return Response(status=HTTPStatus.OK)