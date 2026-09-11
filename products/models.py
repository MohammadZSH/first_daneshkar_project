from django.db import models
from accounts.models import SellerProfile


class Store(models.Model):
    owner = models.ForeignKey(
        SellerProfile,
        on_delete=models.CASCADE,
        related_name='stores'
    )
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Store'
        verbose_name_plural = 'Stores'

    def __str__(self):
        return f"{self.name} (Owner: {self.owner.user.username})"


class Product(models.Model):
    store = models.ForeignKey(
        Store,
        on_delete=models.CASCADE,
        related_name='products'
    )
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='products/%Y/%m/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Product'
        verbose_name_plural = 'Products'

    def __str__(self):
        return f"{self.name} - ${self.price} ({self.store.name})"
