from django.contrib import admin
from .models import Store, Product


class ProductInline(admin.TabularInline):
    model = Product
    extra = 1
    fields = ('name', 'price', 'image')


@admin.register(Store)
class StoreAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'owner', 'created_at')
    search_fields = ('name', 'owner__user__username')
    list_filter = ('created_at',)
    inlines = [ProductInline]


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'store', 'price', 'created_at')
    list_filter = ('store', 'created_at')
    search_fields = ('name', 'description', 'store__name')
