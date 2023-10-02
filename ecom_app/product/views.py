"""
View for product API's.
"""

from core.models import *
from .serializers import *

from http import HTTPStatus

from django.shortcuts import render
from django.urls import reverse
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import viewsets , generics
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


class ProductView(mixins.ListModelMixin,
                viewsets.GenericViewSet):
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


class ProductDetailView(viewsets.ViewSet):
    """"Detail product view for user."""

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def list(self,request: Request, id: int) -> Response:
        prod_obj = Product.objects.filter(id=id)
        serializer = ProductDetailSerializer(prod_obj,many=True)

        return Response(serializer.data)
      

class FavoriteView(mixins.ListModelMixin,
                   viewsets.GenericViewSet):
    """Handle favorite product objects create , update and delete."""
    serializer_class = FavoriteSerializer
    queryset = Favorite.objects.all()
    
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    pagination_class = LargeResultsSetPagination

    def get_queryset(self):
        """Get objects for authenticated user."""
        queryset = self.queryset
        return queryset.filter(user=self.request.user).order_by('-id').distinct()


class FavoriteDetailView(viewsets.ViewSet):
    """Handle favorite objects detail view."""

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def list(self,request: Request, id: int) -> Response:
            favorite_obj = Favorite.objects.filter(id=id,user=request.user)
            serializer = FavoriteDetailSerializer(favorite_obj,many=True)

            return Response(serializer.data)


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


class Remove_from_favorite(APIView):
    """Remove favorite objects."""

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self,request: Request, fav_id: str) -> Response:
        try:
            fav_obj = Favorite.objects.get(id=fav_id,user=request.user)
            fav_obj.delete()
            return Response({'Message':'Item unfavorite!!'})
        
        except:
            return Response({'Message':'Something went wrong or Please check id.'})


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


class Remove_from_cart(APIView):
    """Delete cart item objects."""

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self,request: Request, cart_id: str) -> Response:
        try:
            cart_obj = Cart.objects.get(id=cart_id)
            cart_obj.delete()
            return Response({'Message':'Item remove successfully!!'})

        except:
            return Response({'Message':'Please entre valid id.'})


class Update_from_cart(APIView):
    """Update cart item objects."""

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self,request: Request, cart_id: str) -> Response:
        try:
            cart_obj = Cart.objects.get(id=cart_id,user=request.user)
            cart_obj.quantity += 1
            cart_obj.save()
            return Response({'Message':'Update quantity successfully!!'})
        
        except:
            return Response({'Message':'Please enter valid id.'})


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

        amount = 0
        for c in cart:
            value = c.quantity * c.product.price
            amount = amount + value
        total_price = amount

        my_list = []
        for i in carts:
            my_list.append(str(i.product))
        
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


class OrdersView(APIView):
    """Listing all order objects for authenticated user."""
    
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self,request: Request) -> Response:
        order_obj = OrderPlaced.objects.all()
        order = order_obj.filter(user=self.request.user).order_by('-id').distinct()
        serializer = OrderSerializer(order,many=True)

        if serializer.data == []:
            return Response({'Message':'Not order record found!!'})
        return Response(serializer.data)


class OrderDetailView(APIView):
    """TRy.."""

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request: Request, order_id: str):
        order_obj = OrderPlaced.objects.get(id=order_id,user=request.user)

        if order_obj.status == 'Shipped' or order_obj.status == 'Outer Delivery':
            return Response({'Message':"You can't cancel order!!"})
        elif order_obj.status == 'Delivered':
            if order_obj.paid == True:
                order_obj.delete()
                return Response({'Message':'Your order record deleted!!'})       
        order_obj.delete()
        return Response({'Message':'Order cancel successfully.'})


class Order_Placed(APIView):
    """
    Handle create order objects.
    """

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request: Request):
        serializer = OrderSerializer(data=request.data)
        user_cart = Cart.objects.filter(user=request.user)

        if serializer.is_valid():
            items = [cart.product for cart in user_cart]

            if items == []:
                return Response({'Message':'Please select items..'})
            
            serializer.save(user=request.user, items=items)
            user_cart.delete()
            return Response(serializer.data)
        
        return Response(serializer.errors)


def radhe_radhe(request):
    return render(request,'radhe.html')