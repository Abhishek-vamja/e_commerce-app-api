"""
URL's mapping for product view.
"""

from django.urls import path , include
from product.views import *

from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('view',ProductView)
router.register('create',Product_detail_for_admin)
router.register('cart/my',CartView,basename='cart')
router.register('favorite/my',FavoriteView)
# router.register('addresses/my',AddressView)
router.register('checkout',CheckoutView,basename='checkout')

urlpatterns = [
    path('',include(router.urls)),
    
    path('add_to_cart/<str:product_id>/',Add_to_cart.as_view()),
    path('add_to_favorite/<str:product_id>/',Add_to_favorite.as_view()),

    path('my_order/',Orders.as_view()),
    path('order_placed/<str:cart_id>/',OrderView.as_view()),
]