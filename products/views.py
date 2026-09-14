from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Product, Store, Category
from .forms import StoreForm, ProductForm
from accounts.models import SellerProfile



def home_view(request):
    query = request.GET.get('q', '')
    category_id = request.GET.get('category', '')
    
    products = Product.objects.select_related('store', 'category').order_by('-created_at')
    categories = Category.objects.all()
    
    if query:
        products = products.filter(name__icontains=query) | products.filter(description__icontains=query)
    
    if category_id:
        products = products.filter(category_id=category_id)
    
    return render(request, 'home.html', {
        'products': products,
        'categories': categories,
        'query': query,
        'selected_category': category_id
    })


def stores_list_view(request):
    stores = Store.objects.all().order_by('-created_at')
    return render(request, 'stores.html', {'stores': stores})


def store_detail_view(request, store_id):
    store = get_object_or_404(Store, id=store_id)
    products = store.products.all().order_by('-created_at')
    is_owner = (
        request.user.is_authenticated 
        and hasattr(request.user, 'seller_profile') 
        and (store.owner == request.user.seller_profile or request.user.is_superuser)
    )
    return render(request, 'store_detail.html', {
        'store': store,
        'products': products,
        'is_owner': is_owner
    })


@login_required
def create_store_view(request):
    if not request.user.is_seller and not request.user.is_superuser:
        messages.error(request, "Only sellers can create a store.")
        return redirect('home')
    
    seller, _ = SellerProfile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        form = StoreForm(request.POST)
        if form.is_valid():
            store = form.save(commit=False)
            store.owner = seller
            store.save()
            messages.success(request, "Store created successfully.")
            return redirect('store_detail', store_id=store.id)
    else:
        form = StoreForm()
    return render(request, 'store_form.html', {'form': form})


@login_required
def add_product_view(request, store_id):
    store = get_object_or_404(Store, id=store_id)
    if not request.user.is_superuser and (
        not hasattr(request.user, 'seller_profile') 
        or store.owner != request.user.seller_profile
    ):
        messages.error(request, "You are not allowed to add products to this store.")
        return redirect('store_detail', store_id=store.id)

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.store = store
            product.save()
            messages.success(request, "Product added successfully.")
            return redirect('store_detail', store_id=store.id)
    else:
        form = ProductForm()
    return render(request, 'product_form.html', {'form': form, 'store': store})



@login_required
def edit_product_view(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if not request.user.is_superuser and (
        not hasattr(request.user, 'seller_profile') 
        or product.store.owner != request.user.seller_profile
    ):
        messages.error(request, "You are not allowed to edit this product.")
        return redirect('home')
    
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, "Product updated successfully.")
            return redirect('store_detail', store_id=product.store.id)
    else:
        form = ProductForm(instance=product)
    return render(request, 'product_form.html', {
        'form': form,
        'store': product.store,
        'is_edit': True
    })


@login_required
def delete_product_view(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if not request.user.is_superuser and (
        not hasattr(request.user, 'seller_profile') 
        or product.store.owner != request.user.seller_profile
    ):
        messages.error(request, "You are not allowed to delete this product.")
        return redirect('home')
    
    store_id = product.store.id
    product.delete()
    messages.success(request, "Product deleted successfully.")
    return redirect('store_detail', store_id=store_id)



@login_required
def edit_store_view(request, store_id):
    store = get_object_or_404(Store, id=store_id)
    if not request.user.is_superuser and (
        not hasattr(request.user, 'seller_profile') 
        or store.owner != request.user.seller_profile
    ):
        messages.error(request, "You are not allowed to edit this store.")
        return redirect('home')
    
    if request.method == 'POST':
        form = StoreForm(request.POST, instance=store)
        if form.is_valid():
            form.save()
            messages.success(request, "Store updated successfully.")
            return redirect('store_detail', store_id=store.id)
    else:
        form = StoreForm(instance=store)
    return render(request, 'store_form.html', {'form': form, 'is_edit': True})