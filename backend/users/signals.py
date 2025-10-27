from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from datetime import timedelta

from .models import User


@receiver(post_save, sender=User)
def assign_free_tier_to_new_user(sender, instance, created, **kwargs):
    """
    Automatically assign Basic Plan subscription when user becomes verified
    """
    # Import here to avoid circular import
    from listings.models import PricingPlan, UserSubscription

    # Only create subscription when user becomes verified (not just created)
    if instance.is_verified and not instance.is_superuser:
        # Check if user already has an active subscription
        existing_subscription = UserSubscription.objects.filter(
            userid=instance,
            subscription_status='active'
        ).exists()

        if not existing_subscription:
            try:
                # Get or create Basic plan (plan_price = 0)
                basic_plan, _ = PricingPlan.objects.get_or_create(
                    plan_price=0,
                    defaults={
                        'pricing_name': 'Basic Plan',
                        'pricing_description': 'Perfect for occasional sellers',
                        'duration_days': 60,
                        'category_scope': 'all',
                        'max_listings': 1,
                        'max_images_per_listing': 5,
                        'is_featured': False,
                        'is_active': True,
                    }
                )

                # Create subscription - Basic plan never expires
                UserSubscription.objects.create(
                    userid=instance,
                    pricing_id=basic_plan,
                    subscription_status='active',
                    starts_at=timezone.now(),
                    expires_at=None,  # Basic plan never expires
                    listings_used=0,
                    auto_renew=False
                )

                print(f"✓ Created Basic subscription for user: {instance.email}")
            except Exception as e:
                # Log the error but don't fail user creation
                print(f"Failed to assign Basic Plan to user {instance.userid}: {e}")
