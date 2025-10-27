# SMS Integration Documentation

This document explains the SMS integration using Africa's Talking API for Umuhuza platform.

## Overview

The platform uses **Africa's Talking** SMS gateway to send verification codes and notifications to users in Burundi and across East Africa. In development mode, SMS messages are printed to the console instead of being sent.

---

## Available SMS Functions

### 1. Phone Verification SMS
Send verification code when user registers or requests phone verification.

**Function:** `send_phone_verification_sms(user, code)`

**Usage:**
```python
from users.utils import send_phone_verification_sms

send_phone_verification_sms(user_obj, '123456')
```

**Message Format:**
```
Umuhuza Verification Code: 123456

This code will expire in 10 minutes.

Never share this code with anyone.

- Umuhuza Team
```

---

### 2. Welcome SMS
Send welcome message after successful registration.

**Function:** `send_welcome_sms(user)`

**Usage:**
```python
from users.utils import send_welcome_sms

send_welcome_sms(user_obj)
```

**Message Format:**
```
Welcome to Umuhuza, John!

Your account has been created successfully. Start buying and selling today!

Visit: umuhuza.bi

- Umuhuza Team
```

---

### 3. Password Reset SMS
Send password reset verification code.

**Function:** `send_password_reset_sms(user, code)`

**Usage:**
```python
from users.utils import send_password_reset_sms

send_password_reset_sms(user_obj, '654321')
```

**Message Format:**
```
Umuhuza Password Reset Code: 654321

This code will expire in 10 minutes.

If you didn't request this, please ignore.

- Umuhuza Team
```

---

### 4. Message Notification SMS
Notify user of new message (optional feature).

**Function:** `send_message_notification_sms(recipient, sender_name)`

**Usage:**
```python
from users.utils import send_message_notification_sms

send_message_notification_sms(recipient_user, 'John Doe')
```

**Message Format:**
```
New message from John Doe on Umuhuza!

Login to view and reply: umuhuza.bi/messages

- Umuhuza Team
```

---

## Configuration

### Development Mode (Default)
By default, SMS messages are printed to console:

```python
# settings.py
DEBUG = True
# No Africa's Talking credentials needed
```

**Console Output:**
```
============================================================
📱 SMS MESSAGE
============================================================
To: +25779123456
Message: Umuhuza Verification Code: 123456

This code will expire in 10 minutes.

Never share this code with anyone.

- Umuhuza Team
============================================================
```

---

### Production Mode

#### Step 1: Sign up for Africa's Talking
1. Visit https://africastalking.com
2. Create an account
3. Verify your account
4. Purchase SMS credits

#### Step 2: Get API Credentials
1. Go to your dashboard
2. Navigate to "Settings" → "API Key"
3. Create a new API key
4. Note down your:
   - Username (e.g., `sandbox` or `umuhuza`)
   - API Key (long string of characters)

#### Step 3: Configure Environment Variables

Create a `.env` file in your project root:

```bash
# .env
AFRICAS_TALKING_USERNAME=your_username
AFRICAS_TALKING_API_KEY=your_api_key_here
AFRICAS_TALKING_SENDER_ID=UMUHUZA
```

Or set environment variables directly:

```bash
export AFRICAS_TALKING_USERNAME="your_username"
export AFRICAS_TALKING_API_KEY="your_api_key"
export AFRICAS_TALKING_SENDER_ID="UMUHUZA"
```

#### Step 4: Install Africa's Talking SDK

```bash
pip install africastalking
```

Add to `requirements.txt`:
```
africastalking==1.2.7
```

---

## Integration in Views

### Example 1: Send SMS during registration

```python
# users/views.py

from users.utils import send_phone_verification_sms

@api_view(['POST'])
def register(request):
    serializer = UserRegistrationSerializer(data=request.data)

    if serializer.is_valid():
        user = serializer.save()

        # Generate verification code
        phone_code = generate_code()
        VerificationCode.objects.create(
            userid=user,
            code=phone_code,
            code_type='phone',
            contact_info=user.phone_number,
            expires_at=timezone.now() + timedelta(minutes=10)
        )

        # Send SMS
        send_phone_verification_sms(user, phone_code)

        return Response({
            'message': 'Registration successful! Check your phone for verification code.'
        })

    return Response(serializer.errors, status=400)
```

### Example 2: Resend verification code

```python
# users/views.py

from users.utils import send_phone_verification_sms

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def resend_code(request):
    code_type = request.data.get('code_type')

    if code_type == 'phone':
        # Invalidate old codes
        VerificationCode.objects.filter(
            userid=request.user,
            code_type='phone',
            is_used=False
        ).update(is_used=True)

        # Generate new code
        new_code = generate_code()
        VerificationCode.objects.create(
            userid=request.user,
            code=new_code,
            code_type='phone',
            contact_info=request.user.phone_number,
            expires_at=timezone.now() + timedelta(minutes=10)
        )

        # Send SMS
        send_phone_verification_sms(request.user, new_code)

        return Response({
            'message': 'Verification code sent to your phone'
        })

    return Response({'error': 'Invalid code type'}, status=400)
```

---

## Phone Number Format

Africa's Talking requires phone numbers in international format:

- ✅ **Correct:** `+25779123456` (with country code)
- ❌ **Wrong:** `079123456` (without country code)
- ❌ **Wrong:** `25779123456` (missing + sign)

### Auto-formatting (Recommended)

Add validation to ensure correct format:

```python
def format_phone_number(phone):
    """Format phone number to international format"""
    # Remove spaces and special characters
    phone = ''.join(filter(str.isdigit, phone))

    # Add Burundi country code if not present
    if len(phone) == 8:  # Local format
        phone = '257' + phone

    # Add + sign
    if not phone.startswith('+'):
        phone = '+' + phone

    return phone
```

---

## Costs & Pricing

### Africa's Talking SMS Pricing (Approximate)

| Country | Cost per SMS |
|---------|-------------|
| Burundi | ~$0.05 USD  |
| Kenya   | ~$0.01 USD  |
| Tanzania| ~$0.02 USD  |
| Uganda  | ~$0.02 USD  |
| Rwanda  | ~$0.03 USD  |

**Note:** Prices may vary. Check current pricing at https://africastalking.com/pricing

### Cost Optimization Tips

1. **Only send important SMS** - verification codes, password resets
2. **Use email for less urgent notifications** - marketing, newsletters
3. **Implement rate limiting** - prevent abuse
4. **Set daily SMS limits** per user
5. **Monitor SMS delivery rates** and adjust if needed

---

## Testing

### Test in Development

```bash
python manage.py shell

from users.models import User
from users.utils import send_phone_verification_sms

user = User.objects.first()
send_phone_verification_sms(user, '123456')
```

**Expected Output:**
```
============================================================
📱 SMS MESSAGE
============================================================
To: +25779123456
Message: Umuhuza Verification Code: 123456
...
```

### Test in Sandbox Mode

Africa's Talking provides a sandbox environment:

1. Use username: `sandbox`
2. Use sandbox API key
3. Only whitelisted test numbers will receive SMS
4. Whitelist your test numbers in AT dashboard

---

## Security Best Practices

### 1. Code Expiration
Always set expiration time for verification codes:
```python
expires_at=timezone.now() + timedelta(minutes=10)
```

### 2. Rate Limiting
Limit SMS per user per day:
```python
# Check recent SMS count
recent_codes = VerificationCode.objects.filter(
    userid=user,
    code_type='phone',
    createdat__gte=timezone.now() - timedelta(hours=24)
).count()

if recent_codes >= 5:
    return Response({'error': 'Too many SMS requests. Try again tomorrow.'})
```

### 3. Code Validation
Validate codes securely:
```python
verification = VerificationCode.objects.get(
    userid=user,
    code=code,
    code_type='phone',
    is_used=False
)

if not verification.is_valid():
    return Response({'error': 'Code expired'})
```

### 4. Never Log SMS Content
Don't log SMS messages or codes in production logs.

---

## Troubleshooting

### SMS not sending?
1. Check Africa's Talking credentials in `.env`
2. Verify phone number format (must include +)
3. Check SMS credits balance
4. Verify API key permissions
5. Check AT dashboard for error logs

### SMS not received?
1. Check phone number is correct
2. Verify phone is on and has signal
3. Check SMS wasn't blocked as spam
4. Try different phone number
5. Check AT delivery reports

### Invalid phone number error?
1. Ensure phone number is in format: `+25779123456`
2. Verify country code is correct (257 for Burundi)
3. Check phone number length is correct

### API authentication failed?
1. Verify `AFRICAS_TALKING_USERNAME` is correct
2. Check `AFRICAS_TALKING_API_KEY` has no extra spaces
3. Regenerate API key in AT dashboard if needed

---

## Monitoring & Analytics

### Track SMS Delivery

```python
# In send_sms function
try:
    response = sms.send(message=message, recipients=[phone_number])

    # Log response
    print(f"SMS Response: {response}")

    # Check status
    for recipient in response['SMSMessageData']['Recipients']:
        status = recipient['status']  # 'Success' or 'Failed'
        cost = recipient['cost']
        message_id = recipient['messageId']

        # Store in database for analytics
        SMSLog.objects.create(
            phone_number=phone_number,
            status=status,
            cost=cost,
            message_id=message_id
        )

    return True
except Exception as e:
    print(f"SMS Error: {str(e)}")
    return False
```

### Useful Metrics to Track

- SMS sent per day
- SMS delivery rate
- SMS costs per month
- Failed SMS reasons
- Average delivery time
- User verification completion rate

---

## Alternative SMS Providers

If Africa's Talking doesn't work for your region, consider:

1. **Twilio** - Global coverage, higher costs
2. **Vonage (Nexmo)** - Good for East Africa
3. **Infobip** - Enterprise solution
4. **ClickSend** - Affordable rates
5. **BulkSMS** - Popular in Africa

Integration is similar - just replace Africa's Talking SDK calls.

---

## Future Enhancements

- [ ] Add SMS delivery tracking
- [ ] Implement SMS templates in database
- [ ] Add multi-language SMS support (Kirundi, French)
- [ ] Create SMS analytics dashboard
- [ ] Add SMS scheduling
- [ ] Implement SMS webhooks for delivery reports
- [ ] Add cost monitoring and alerts
- [ ] Create SMS rate limiting middleware
- [ ] Add A/B testing for SMS content
- [ ] Implement SMS fallback for failed deliveries

---

## Support

For issues with:
- **Umuhuza SMS integration:** Contact dev team
- **Africa's Talking API:** Visit https://help.africastalking.com
- **SMS delivery issues:** Check AT dashboard logs
- **Pricing questions:** Contact AT sales team

---

## Quick Reference

```python
# Send phone verification code
from users.utils import send_phone_verification_sms
send_phone_verification_sms(user, '123456')

# Send welcome SMS
from users.utils import send_welcome_sms
send_welcome_sms(user)

# Send password reset code
from users.utils import send_password_reset_sms
send_password_reset_sms(user, '654321')

# Send message notification
from users.utils import send_message_notification_sms
send_message_notification_sms(recipient, sender_name)
```

---

**Last Updated:** 2025-01-22

**Documentation maintained by:** Umuhuza Development Team
