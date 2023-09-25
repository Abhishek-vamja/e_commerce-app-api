"""
URL's mapping for product view.
"""

from django.urls import path , include
from product.views import *

from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('view',product)
router.register('addresses/my',AddressView)
router.register('create',Product_detail_for_admin)
router.register('checkout',checkout)
router.register('favorite/my',FavoriteView)

urlpatterns = [
    path('',include(router.urls)),
    
    path('favorite/<str:product_id>/',Create_favorite.as_view()),
]