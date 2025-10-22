# Email Templates Documentation

This directory contains HTML email templates for the Umuhuza platform.

## Available Templates

### 1. Welcome Email (`welcome.html`)
Sent when a user registers for the first time.

**Usage:**
```python
from users.utils import send_welcome_email

send_welcome_email(
    user=user_obj,
    verification_url='http://localhost:5173/verify?token=abc123'
)
```

**Template Variables:**
- `user_name`: Full name of the user
- `verification_url`: URL to verify email
- `base_url`: Frontend base URL

---

### 2. Email Verification (`verify_email.html`)
Sent to verify user's email address.

**Usage:**
```python
from users.utils import send_verification_email

send_verification_email(
    user=user_obj,
    verification_url='http://localhost:5173/verify?token=abc123',
    verification_code='ABC123'
)
```

**Template Variables:**
- `user_name`: Full name of the user
- `verification_url`: URL to verify email
- `verification_code`: 6-digit verification code
- `base_url`: Frontend base URL

---

### 3. Password Reset (`password_reset.html`)
Sent when user requests password reset.

**Usage:**
```python
from users.utils import send_password_reset_email

send_password_reset_email(
    user=user_obj,
    reset_url='http://localhost:5173/reset-password?token=xyz789'
)
```

**Template Variables:**
- `user_name`: Full name of the user
- `reset_url`: URL to reset password
- `base_url`: Frontend base URL

---

### 4. New Message Notification (`new_message.html`)
Sent when user receives a new message.

**Usage:**
```python
from users.utils import send_new_message_email

send_new_message_email(
    recipient=recipient_user,
    sender=sender_user,
    message_content='Hello, is this still available?',
    listing=listing_obj,  # Optional
    chat_url='http://localhost:5173/messages?chat=123'
)
```

**Template Variables:**
- `recipient_name`: Recipient's full name
- `sender_name`: Sender's full name
- `sender_initials`: Sender's initials for avatar
- `message_content`: Message text
- `sent_time`: Formatted timestamp
- `listing_title`: Listing title (optional)
- `listing_price`: Listing price (optional)
- `chat_url`: URL to chat
- `base_url`: Frontend base URL

---

### 5. New Review Notification (`new_review.html`)
Sent when user receives a new review.

**Usage:**
```python
from users.utils import send_new_review_email

send_new_review_email(
    recipient=reviewed_user,
    reviewer=reviewer_user,
    rating=5,
    comment='Great seller, highly recommended!',
    average_rating=4.7,
    total_reviews=23,
    profile_url='http://localhost:5173/profile'
)
```

**Template Variables:**
- `recipient_name`: Recipient's full name
- `reviewer_name`: Reviewer's full name
- `reviewer_initials`: Reviewer's initials for avatar
- `stars`: Star rating display (⭐⭐⭐⭐⭐)
- `review_comment`: Review comment text (optional)
- `review_date`: Review date
- `average_rating`: User's average rating
- `total_reviews`: Total number of reviews
- `profile_url`: URL to user's profile
- `base_url`: Frontend base URL

---

## Email Configuration

### Development
Emails are logged to the console using Django's `console` backend.

### Production
To send real emails in production, update `settings.py`:

```python
# Email settings for production
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'  # or your SMTP server
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'your-email@gmail.com'
EMAIL_HOST_PASSWORD = 'your-app-password'
DEFAULT_FROM_EMAIL = 'noreply@umuhuza.bi'
```

### Environment Variables
```bash
# .env file
FRONTEND_URL=https://umuhuza.bi
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
```

---

## Integration Examples

### Example 1: Send welcome email after registration
```python
# In users/views.py - register view

from users.utils import send_welcome_email
from django.contrib.auth.tokens import default_token_generator

@api_view(['POST'])
def register(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()

        # Generate verification token
        token = default_token_generator.make_token(user)
        verification_url = f"{settings.FRONTEND_URL}/verify?token={token}&uid={user.userid}"

        # Send welcome email
        send_welcome_email(user, verification_url)

        return Response({'message': 'User registered successfully'})
    return Response(serializer.errors, status=400)
```

### Example 2: Send notification when message is received
```python
# In messaging/views.py - send message view

from users.utils import send_new_message_email

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def send_message(request):
    # ... create message logic ...

    # Send email notification to recipient
    send_new_message_email(
        recipient=message.recipient,
        sender=request.user,
        message_content=message.message_text,
        listing=message.listing,
        chat_url=f"{settings.FRONTEND_URL}/messages?chat={message.chatid}"
    )

    return Response({'message': 'Message sent'})
```

### Example 3: Send notification when review is created
```python
# In listings/views.py - create review view

from users.utils import send_new_review_email
from django.db.models import Avg

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_review(request):
    # ... create review logic ...

    # Calculate new average rating
    reviews = RatingReview.objects.filter(reviewed_userid=reviewed_user, is_visible=True)
    avg_rating = reviews.aggregate(Avg('rating'))['rating__avg'] or 0
    total_reviews = reviews.count()

    # Send email notification
    send_new_review_email(
        recipient=reviewed_user,
        reviewer=request.user,
        rating=review.rating,
        comment=review.comment,
        average_rating=avg_rating,
        total_reviews=total_reviews,
        profile_url=f"{settings.FRONTEND_URL}/users/{reviewed_user.userid}"
    )

    return Response({'message': 'Review submitted'})
```

---

## Testing Emails

### Test in Django Shell
```python
python manage.py shell

from users.models import User
from users.utils import send_welcome_email

user = User.objects.first()
send_welcome_email(user, 'http://localhost:5173/verify?token=test123')
```

### Check Console Output
When using the console backend, emails will be printed to the terminal where Django is running.

---

## Customization

All templates use the same color scheme and branding:
- **Primary Color**: `#667eea` (purple)
- **Secondary Color**: `#764ba2` (dark purple)
- **Font**: System fonts (-apple-system, etc.)

To customize templates, edit the HTML files directly. All styles are inline for maximum email client compatibility.

---

## Email Client Compatibility

These templates are tested and work with:
- Gmail (web, mobile)
- Outlook (web, desktop)
- Apple Mail (macOS, iOS)
- Yahoo Mail
- Thunderbird

They use inline styles and table-based layouts for maximum compatibility with older email clients.

---

## Best Practices

1. **Keep file sizes small** - Images should be optimized and minimal
2. **Use inline styles** - External CSS doesn't work in most email clients
3. **Test before sending** - Always test emails in multiple clients
4. **Provide plain text fallback** - The `message` parameter in `send_mail()` is the fallback
5. **Use responsive design** - Templates work on mobile and desktop
6. **Include unsubscribe links** - Required for production emails (add to footer)

---

## Troubleshooting

### Emails not sending?
1. Check `EMAIL_BACKEND` in settings.py
2. Verify SMTP credentials
3. Check Django logs for errors
4. Test SMTP connection separately

### Emails going to spam?
1. Set up SPF, DKIM, and DMARC records
2. Use a verified sending domain
3. Avoid spam trigger words
4. Include proper headers and unsubscribe links

### Template not rendering?
1. Check template path is correct
2. Verify template variables are provided
3. Check Django template loader configuration
4. Look for syntax errors in template

---

## Future Enhancements

- [ ] Add email preferences/unsubscribe functionality
- [ ] Create digest emails (daily/weekly summaries)
- [ ] Add promotional email templates
- [ ] Implement email tracking (opens, clicks)
- [ ] Create admin notification templates
- [ ] Add multi-language support (Kirundi, French)
- [ ] Create SMS notification fallbacks
