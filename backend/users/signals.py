from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from datetime import timedelta

from .models import User


@receiver(post_save, sender=User)
def assign_free_tier_to_new_user(sender, instance, created, **kwargs):
    """
    Automatically assign free tier subscription when a new user is created
    """
    # Import here to avoid circular import
    from listings.models import PricingPlan, UserSubscription

    if created and not instance.is_superuser:
        # Get the free tier pricing plan (pricing_name='Free Tier' or plan_price=0)
        try:
            free_tier = PricingPlan.objects.filter(
                pricing_name='Free Tier',
                plan_price=0,
                is_active=True
            ).first()

            if free_tier:
                # Create subscription for the user
                starts_at = timezone.now()
                expires_at = starts_at + timedelta(days=free_tier.duration_days)

                UserSubscription.objects.create(
                    userid=instance,
                    pricing_id=free_tier,
                    subscription_status='active',
                    starts_at=starts_at,
                    expires_at=expires_at,
                    listings_used=0,
                    auto_renew=False
                )
        except Exception as e:
            # Log the error but don't fail user creation
            print(f"Failed to assign free tier to user {instance.userid}: {e}")
