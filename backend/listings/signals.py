from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Listing


@receiver(post_save, sender=Listing)
def set_user_as_seller(sender, instance, created, **kwargs):
    """
    Automatically set is_seller flag when user creates their first listing
    """
    if created and instance.userid:
        user = instance.userid
        if not user.is_seller:
            user.is_seller = True
            # Update legacy role field if still 'buyer'
            if user.user_role == 'buyer':
                user.user_role = 'seller'
            user.save(update_fields=['is_seller', 'user_role'])
