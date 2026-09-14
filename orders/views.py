from decimal import Decimal
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction
from .models import CartItem, Order, OrderItem
from products.models import Product
from accounts.models import CustomerProfile, SellerProfile


@login_required
def order_history(request):
    orders = Order.objects.filter(customer__user=request.user).order_by('-date').prefetch_related('items__product')
    return render(request, 'order_history.html', {'orders': orders})

# 6. Cart Page
@login_required
def cart_view(request):
    customer, _ = CustomerProfile.objects.get_or_create(user=request.user)
    cart_items = CartItem.objects.filter(customer=customer).select_related('product', 'product__store')
    total_price = sum(item.total_price for item in cart_items)
    
    return render(request, 'cart.html', {
        'cart_items': cart_items,
        'total_price': total_price,
        'customer': customer
    })


@login_required
def add_to_cart_view(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    customer, _ = CustomerProfile.objects.get_or_create(user=request.user)

    cart_item, created = CartItem.objects.get_or_create(customer=customer, product=product)
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    
    messages.success(request, f"«{product.name}» به سبد خرید اضافه شد.")
    # Redirect back to where the request came from or home
    return redirect(request.META.get('HTTP_REFERER', 'home'))


@login_required
def remove_from_cart_view(request, item_id):
    customer, _ = CustomerProfile.objects.get_or_create(user=request.user)
    cart_item = get_object_or_404(CartItem, id=item_id, customer=customer)
    cart_item.delete()
    messages.info(request, "محصول از سبد خرید حذف شد.")
    return redirect('cart')


# Checkout transaction: Deducts from Customer balance and completes order
@login_required
def checkout_view(request):
    customer, _ = CustomerProfile.objects.get_or_create(user=request.user)
    cart_items = CartItem.objects.filter(customer=customer).select_related('product', 'product__store__owner')

    if not cart_items.exists():
        messages.error(request, "سبد خرید شما خالی است.")
        return redirect('cart')

    total_amount = sum(item.total_price for item in cart_items)

    if customer.balance < total_amount:
        messages.error(request, f"موجودی شما کافی نیست! موجودی: {customer.balance} | مبلغ کل: {total_amount}")
        return redirect('payment')

    with transaction.atomic():
        # 1. Deduct customer balance
        customer.balance -= total_amount
        customer.save()

        # 2. Create Order
        order = Order.objects.create(
            customer=customer,
            total_amount=total_amount,
            status=Order.STATUS_PAID
        )

        # 3. Create OrderItems
        for item in cart_items:
            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                price=item.product.price
            )

        # 4. Clear cart
        cart_items.delete()

    messages.success(request, f"Сفارش شماره #{order.id} با موفقیت ثبت و پرداخت شد.")
    return redirect('customer_panel')