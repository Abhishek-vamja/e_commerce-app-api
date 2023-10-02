"""
URL's mapping for product view.
"""

from django.urls import path , include
from product.views import *

from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('view',ProductView)
router.register('cart/my',CartView,basename='cart')
router.register('favorite/my',FavoriteView,basename='favorite')
router.register('checkout',CheckoutView,basename='checkout')

urlpatterns = [
    path('',include(router.urls)),
    
    path('view/<int:id>/',ProductDetailView.as_view({'get':'list'})),
    
    path('add_to_cart/<str:product_id>/',Add_to_cart.as_view()),
    path('cart/my/remove/<str:cart_id>/',Remove_from_cart.as_view()),
    path('cart/my/update/<str:cart_id>/',Update_from_cart.as_view()),

    path('favorite/my/<int:id>/',FavoriteDetailView.as_view({'get':'list'})),
    path('add_to_favorite/<str:product_id>/',Add_to_favorite.as_view()),
    path('favorite/my/remove/<str:fav_id>/',Remove_from_favorite.as_view()),
    
    path('orders/',OrdersView.as_view()),
    path('orders/cancel/<str:order_id>/',OrderDetailView.as_view()),
    path('order_placed/',Order_Placed.as_view(),name='order_placed'),
]