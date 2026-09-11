from django import forms
from .models import Store, Product


class StoreForm(forms.ModelForm):
    class Meta:
        model = Store
        fields = ['name', 'description']


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'price', 'description', 'image']
