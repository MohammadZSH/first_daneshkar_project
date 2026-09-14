from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Product, Store
from .forms import StoreForm, ProductForm
from accounts.models import SellerProfile


# 1. Landing Page: All products sorted newest first
def home_view(request):
    products = Product.objects.select_related('store').order_by('-created_at')
    return render(request, 'home.html', {'products': products})


# 2. Stores Page: List of all stores
def stores_list_view(request):
    stores = Store.objects.all().order_by('-created_at')
    return render(request, 'stores.html', {'stores': stores})


# 3. Store Detail Page
def store_detail_view(request, store_id):
    store = get_object_or_404(Store, id=store_id)
    products = store.products.all().order_by('-created_at')
    is_owner = request.user.is_authenticated and hasattr(request.user, 'seller_profile') and (store.owner == request.user.seller_profile or request.user.is_superuser)
    return render(request, 'store_detail.html', {
        'store': store,
        'products': products,
        'is_owner': is_owner
    })


# Create a new store (Seller only)
@login_required
def create_store_view(request):
    if not request.user.is_seller and not request.user.is_superuser:
        messages.error(request, "تنها فروشندگان می‌توانند فروشگاه ایجاد کنند.")
        return redirect('home')
    
    seller, _ = SellerProfile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        form = StoreForm(request.POST)
        if form.is_valid():
            store = form.save(commit=False)
            store.owner = seller
            store.save()
            messages.success(request, "فروشگاه با موفقیت ایجاد شد.")
            return redirect('store_detail', store_id=store.id)
    else:
        form = StoreForm()
    return render(request, 'store_detail.html', {'form': form, 'is_create': True})


# Add Product to a Store (Seller only)
@login_required
def add_product_view(request, store_id):
    store = get_object_or_404(Store, id=store_id)
    if not request.user.is_superuser and (not hasattr(request.user, 'seller_profile') or store.owner != request.user.seller_profile):
        messages.error(request, "شما اجازه افزودن محصول به این فروشگاه را ندارید.")
        return redirect('store_detail', store_id=store.id)

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.store = store
            product.save()
            messages.success(request, "محصول با موفقیت افزوده شد.")
            return redirect('store_detail', store_id=store.id)
    else:
        form = ProductForm()
    return render(request, 'store_detail.html', {'form': form, 'store': store, 'is_add_product': True})
