from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Listing


@receiver(post_save, sender=Listing)
def set_user_as_seller(sender, instance, created, **kwargs):
    """
    Automatically promote user from 'buyer' to 'seller' when they create their first listing.
    This allows users to be both buyers and sellers on the platform.
    """
    if created and instance.userid:
        user = instance.userid

        # If user is currently a buyer, promote them to seller
        if user.user_role == 'buyer':
            user.user_role = 'seller'
            user.save(update_fields=['user_role'])
