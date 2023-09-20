from django.contrib import admin

# Register your models here.
from core.models import Category,Product

admin.site.register(Category)
admin.site.register(Product)