from django.utils import timezone
from datetime import timedelta
from .models import UserBadge


def award_badge(user, badge_type, expires_days=None):
    """
    Award a badge to a user
    """
    expires_at = None
    if expires_days:
        expires_at = timezone.now() + timedelta(days=expires_days)
    
    badge, created = UserBadge.objects.get_or_create(
        userid=user,
        badge_type=badge_type,
        defaults={'expires_at': expires_at}
    )
    
    if not created and expires_days:
        # Update expiration if badge already exists
        badge.expires_at = expires_at
        badge.save()
    
    return badge


def check_and_award_badges(user):
    """
    Check user activity and award appropriate badges
    """
    from listings.models import Listing, RatingReview
    from django.db.models import Avg
    
    # Verified Badge (both email and phone verified)
    if user.email_verified and user.phone_verified and not user.is_verified:
        user.is_verified = True
        user.save()
        award_badge(user, 'verified')
    
    # Trusted Seller Badge (5+ listings, avg rating 4+)
    if user.user_role == 'seller':
        listing_count = Listing.objects.filter(userid=user, listing_status='active').count()
        avg_rating = RatingReview.objects.filter(
            reviewed_userid=user,
            is_visible=True
        ).aggregate(Avg('rating'))['rating__avg'] or 0
        
        if listing_count >= 5 and avg_rating >= 4.0:
            award_badge(user, 'trusted_seller', expires_days=365)
    
    # Top Dealer Badge (10+ active listings, dealer role)
    if user.user_role == 'dealer':
        listing_count = Listing.objects.filter(userid=user, listing_status='active').count()
        if listing_count >= 10:
            award_badge(user, 'top_dealer', expires_days=365)


def revoke_badge(user, badge_type):
    """
    Revoke a badge from a user
    """
    UserBadge.objects.filter(userid=user, badge_type=badge_type).delete()