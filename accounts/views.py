from decimal import Decimal
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction
from .forms import SignUpForm, AddBalanceForm
from .models import SellerProfile, CustomerProfile
from orders.models import Order

@login_required
def order_history(request):
    orders = Order.objects.filter(customer__user=request.user).order_by('-created_at').prefetch_related('items__product')
    return render(request, 'order_history.html', {'orders': orders})


def signup_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "ثبت نام با موفقیت انجام شد.")
            if user.is_seller:
                return redirect('seller_panel')
            return redirect('customer_panel')
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form})


def logout_view(request):
    logout(request)
    return render(request, 'registration/logged_out.html')


@login_required
def customer_panel(request):
    # Ensure profile exists
    customer, _ = CustomerProfile.objects.get_or_create(user=request.user)
    orders = Order.objects.filter(customer=customer).prefetch_related('items__product').order_by('-date')
    return render(request, 'customer_panel.html', {
        'customer': customer,
        'orders': orders
    })


@login_required
def seller_panel(request):
    if not request.user.is_seller and not request.user.is_superuser:
        messages.error(request, "شما دسترسی فروشنده ندارید.")
        return redirect('home')
    
    seller, _ = SellerProfile.objects.get_or_create(user=request.user)
    stores = seller.stores.all()
    return render(request, 'seller_panel.html', {
        'seller': seller,
        'stores': stores
    })


@login_required
def payment_view(request):
    customer, _ = CustomerProfile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        form = AddBalanceForm(request.POST)
        if form.is_valid():
            amount = form.cleaned_data['amount']
            customer.balance += amount
            customer.save()
            messages.success(request, f"مبلغ {amount} با موفقیت به موجودی شما افزوده شد.")
            return redirect('customer_panel')
    else:
        form = AddBalanceForm()
    return render(request, 'payment.html', {'form': form, 'customer': customer})
