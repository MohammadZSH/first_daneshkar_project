from django.contrib import admin
from .models import CartItem, Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    fields = ('product', 'quantity', 'price', 'get_subtotal')
    readonly_fields = ('get_subtotal',)

    @admin.display(description='Subtotal')
    def get_subtotal(self, obj):
        return f"${obj.subtotal:.2f}" if obj.pk else "-"


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer', 'total_amount', 'status', 'date')
    list_filter = ('status', 'date')
    search_fields = ('id', 'customer__user__username')
    readonly_fields = ('date', 'updated_at')
    inlines = [OrderItemInline]


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer', 'product', 'quantity', 'get_total_price', 'added_at')
    list_filter = ('added_at',)
    search_fields = ('customer__user__username', 'product__name')

    @admin.display(description='Total Price')
    def get_total_price(self, obj):
        return f"${obj.total_price:.2f}"
