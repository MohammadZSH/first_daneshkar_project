from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import User, CustomerProfile, SellerProfile


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        # Automatically create CustomerProfile
        CustomerProfile.objects.create(user=instance)

        # Automatically create SellerProfile if flagged as seller
        if instance.is_seller:
            SellerProfile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    # Ensure profile exists if is_seller gets turned on later
    if instance.is_seller and not hasattr(instance, 'seller_profile'):
        SellerProfile.objects.create(user=instance)

    # Save existing profiles if they exist
    if hasattr(instance, 'customer_profile'):
        instance.customer_profile.save()
    if hasattr(instance, 'seller_profile'):
        instance.seller_profile.save()
