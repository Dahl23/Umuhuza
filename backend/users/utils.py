from django.utils import timezone
from datetime import timedelta
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
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


# ============================================================================
# SMS UTILITIES
# ============================================================================

def send_sms(phone_number, message):
    """
    Send SMS using Africa's Talking API

    For development, SMS content is printed to console.
    For production, configure Africa's Talking credentials.
    """
    # Development mode - print to console
    if settings.DEBUG or not hasattr(settings, 'AFRICAS_TALKING_USERNAME'):
        print(f"\n{'='*60}")
        print(f"📱 SMS MESSAGE")
        print(f"{'='*60}")
        print(f"To: {phone_number}")
        print(f"Message: {message}")
        print(f"{'='*60}\n")
        return True

    # Production mode - use Africa's Talking
    try:
        import africastalking

        # Initialize SDK
        africastalking.initialize(
            username=settings.AFRICAS_TALKING_USERNAME,
            api_key=settings.AFRICAS_TALKING_API_KEY
        )

        # Get SMS service
        sms = africastalking.SMS

        # Send SMS
        response = sms.send(
            message=message,
            recipients=[phone_number],
            sender_id=getattr(settings, 'AFRICAS_TALKING_SENDER_ID', None)
        )

        return True
    except Exception as e:
        print(f"Error sending SMS: {str(e)}")
        return False


def send_phone_verification_sms(user, code):
    """
    Send phone verification code via SMS
    """
    message = f"""Umuhuza Verification Code: {code}

This code will expire in 10 minutes.

Never share this code with anyone.

- Umuhuza Team"""

    return send_sms(user.phone_number, message)


def send_welcome_sms(user):
    """
    Send welcome SMS to new user
    """
    message = f"""Welcome to Umuhuza, {user.user_firstname}!

Your account has been created successfully. Start buying and selling today!

Visit: umuhuza.bi

- Umuhuza Team"""

    return send_sms(user.phone_number, message)


def send_password_reset_sms(user, code):
    """
    Send password reset code via SMS
    """
    message = f"""Umuhuza Password Reset Code: {code}

This code will expire in 10 minutes.

If you didn't request this, please ignore.

- Umuhuza Team"""

    return send_sms(user.phone_number, message)


def send_message_notification_sms(recipient, sender_name):
    """
    Notify user of new message via SMS
    """
    message = f"""New message from {sender_name} on Umuhuza!

Login to view and reply: umuhuza.bi/messages

- Umuhuza Team"""

    return send_sms(recipient.phone_number, message)


# ============================================================================
# EMAIL UTILITIES
# ============================================================================

def send_welcome_email(user, verification_url):
    """
    Send welcome email to new user
    """
    context = {
        'user_name': user.full_name,
        'verification_url': verification_url,
        'base_url': settings.FRONTEND_URL or 'http://localhost:5173',
    }

    html_message = render_to_string('emails/welcome.html', context)

    send_mail(
        subject='Welcome to Umuhuza!',
        message=f'Welcome {user.full_name}! Please verify your email: {verification_url}',
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[user.email],
        html_message=html_message,
        fail_silently=False,
    )


def send_verification_email(user, verification_url, verification_code):
    """
    Send email verification link to user
    """
    context = {
        'user_name': user.full_name,
        'verification_url': verification_url,
        'verification_code': verification_code,
        'base_url': settings.FRONTEND_URL or 'http://localhost:5173',
    }

    html_message = render_to_string('emails/verify_email.html', context)

    send_mail(
        subject='Verify Your Email - Umuhuza',
        message=f'Hi {user.full_name}, please verify your email: {verification_url}',
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[user.email],
        html_message=html_message,
        fail_silently=False,
    )


def send_password_reset_email(user, reset_url):
    """
    Send password reset email to user
    """
    context = {
        'user_name': user.full_name,
        'reset_url': reset_url,
        'base_url': settings.FRONTEND_URL or 'http://localhost:5173',
    }

    html_message = render_to_string('emails/password_reset.html', context)

    send_mail(
        subject='Reset Your Password - Umuhuza',
        message=f'Hi {user.full_name}, reset your password: {reset_url}',
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[user.email],
        html_message=html_message,
        fail_silently=False,
    )


def send_new_message_email(recipient, sender, message_content, listing=None, chat_url=None):
    """
    Notify user of new message
    """
    from datetime import datetime

    context = {
        'recipient_name': recipient.full_name,
        'sender_name': sender.full_name,
        'sender_initials': f'{sender.user_firstname[0]}{sender.user_lastname[0]}'.upper(),
        'message_content': message_content,
        'sent_time': datetime.now().strftime('%B %d, %Y at %I:%M %p'),
        'listing_title': listing.listing_title if listing else None,
        'listing_price': listing.listing_price if listing else None,
        'chat_url': chat_url or f"{settings.FRONTEND_URL}/messages",
        'base_url': settings.FRONTEND_URL or 'http://localhost:5173',
    }

    html_message = render_to_string('emails/new_message.html', context)

    send_mail(
        subject=f'New message from {sender.full_name} - Umuhuza',
        message=f'{sender.full_name} sent you a message: {message_content[:100]}...',
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[recipient.email],
        html_message=html_message,
        fail_silently=True,  # Don't break if email fails
    )


def send_new_review_email(recipient, reviewer, rating, comment, average_rating, total_reviews, profile_url=None):
    """
    Notify user of new review
    """
    from datetime import datetime

    # Generate star rating display
    stars = '⭐' * rating + '☆' * (5 - rating)

    context = {
        'recipient_name': recipient.full_name,
        'reviewer_name': reviewer.full_name,
        'reviewer_initials': f'{reviewer.user_firstname[0]}{reviewer.user_lastname[0]}'.upper(),
        'stars': stars,
        'review_comment': comment,
        'review_date': datetime.now().strftime('%B %d, %Y'),
        'average_rating': f'{average_rating:.1f}',
        'total_reviews': total_reviews,
        'profile_url': profile_url or f"{settings.FRONTEND_URL}/profile",
        'base_url': settings.FRONTEND_URL or 'http://localhost:5173',
    }

    html_message = render_to_string('emails/new_review.html', context)

    send_mail(
        subject=f'New {rating}-star review from {reviewer.full_name} - Umuhuza',
        message=f'{reviewer.full_name} left you a {rating}-star review!',
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[recipient.email],
        html_message=html_message,
        fail_silently=True,  # Don't break if email fails
    )