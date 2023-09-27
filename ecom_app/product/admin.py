from django.contrib import admin

from core.models import Category,Product,Cart,Favorite,Checkout,OrderPlaced

admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Cart)
admin.site.register(Favorite)
admin.site.register(Checkout)
admin.site.register(OrderPlaced)