from django.contrib import admin
from .models import Product,  Category,ProductVariant


class ProductVariationInline(admin.TabularInline):
    model = ProductVariant
    extra = 1  # Number of empty variations to display by default

class ProductAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name', 'description']

    inlines = [ProductVariationInline]


admin.site.register(Product, ProductAdmin)
admin.site.register(Category)
