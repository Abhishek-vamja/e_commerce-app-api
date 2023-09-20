from django.contrib import admin

from core.models import Category,Product,Cart,Address,Favorite,CheckOut

admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Cart)
admin.site.register(Address)
admin.site.register(Favorite)
admin.site.register(CheckOut)