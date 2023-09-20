"""
URL's mapping for product view.
"""

from django.urls import path , include
from product.views import *

from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('details',ProductDetail)

urlpatterns = [
    path('view/',ProductView.as_view({'get': 'list'}),name='products'),

    path('',include(router.urls))
]