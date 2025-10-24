from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone

from .models import DealerApplication


@receiver(post_save, sender=DealerApplication)
def promote_to_dealer_on_approval(sender, instance, created, **kwargs):
    """
    Automatically promote user to dealer when their application is approved
    """
    if not created and instance.appli_status == 'approved':
        user = instance.userid

        # Update user to dealer
        if not user.is_dealer:
            user.is_dealer = True
            user.user_role = 'dealer'
            user.save(update_fields=['is_dealer', 'user_role'])

            # Set approval timestamp if not set
            if not instance.approvedat:
                instance.approvedat = timezone.now()
                instance.save(update_fields=['approvedat'])
