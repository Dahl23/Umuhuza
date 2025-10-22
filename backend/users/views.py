from django.shortcuts import render

from umuhuza_api import settings
from .utils import check_and_award_badges
from notifications.utils import notify_verification_complete
from rest_framework import status, generics
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from django.utils import timezone
from datetime import timedelta
import random
import string

from .models import User, VerificationCode
from .serializers import (
    UserRegistrationSerializer,
    UserProfileSerializer,
    VerificationCodeSerializer,
    ResendCodeSerializer
)


def generate_code(length=6):
    """Generate random verification code"""
    return ''.join(random.choices(string.digits, k=length))


def get_tokens_for_user(user):
    """Generate JWT tokens for user"""
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


@api_view(['POST'])
@permission_classes([AllowAny])
def register_view(request):
    """
    Register a new user
    POST /api/auth/register/
    {
        "user_firstname": "John",
        "user_lastname": "Doe",
        "email": "john@example.com",
        "phone_number": "+25779123456",
        "password": "SecurePass123",
        "password_confirm": "SecurePass123"
    }
    """
    serializer = UserRegistrationSerializer(data=request.data)
    
    if serializer.is_valid():
        user = serializer.save()
        
        # Always generate BOTH codes
        email_code = generate_code()
        VerificationCode.objects.create(
            userid=user,
            code=email_code,
            code_type='email',
            contact_info=user.email,
            expires_at=timezone.now() + timedelta(minutes=15)
        )
        
        phone_code = generate_code()
        VerificationCode.objects.create(
            userid=user,
            code=phone_code,
            code_type='phone',
            contact_info=user.phone_number,
            expires_at=timezone.now() + timedelta(minutes=10)
        )
        
        # Send verification codes
        from .utils import send_phone_verification_sms
        send_phone_verification_sms(user, phone_code)

        # Email sending will be implemented later
        print(f"📧 Email verification code for {user.email}: {email_code}")
        
        # Generate tokens
        tokens = get_tokens_for_user(user)
        
        return Response({
            'message': 'Registration successful! Please verify your email and phone.',
            'user': UserProfileSerializer(user).data,
            'tokens': tokens,
            # Only include codes in development
            'email_code': email_code if settings.DEBUG else None,
            'phone_code': phone_code if settings.DEBUG else None,
        }, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
    """
    Login user
    POST /api/auth/login/
    {
        "email": "john@example.com",
        "password": "SecurePass123"
    }
    """
    email = request.data.get('email')
    password = request.data.get('password')
    
    if not email or not password:
        return Response({
            'error': 'Please provide both email and password'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    user = authenticate(request, email=email, password=password)
    
    if user is not None:
        if not user.is_active:
            return Response({
                'error': 'Account is deactivated'
            }, status=status.HTTP_403_FORBIDDEN)
        
        # Update last login
        user.last_login = timezone.now()
        user.save(update_fields=['last_login'])
        
        # Generate tokens
        tokens = get_tokens_for_user(user)
        
        return Response({
            'message': 'Login successful',
            'user': UserProfileSerializer(user).data,
            'tokens': tokens
        }, status=status.HTTP_200_OK)
    
    return Response({
        'error': 'Invalid email or password'
    }, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_view(request):
    """
    Logout user (client should delete tokens)
    POST /api/auth/logout/
    """
    return Response({
        'message': 'Logout successful'
    }, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def verify_email_view(request):
    """
    Verify email with code
    POST /api/auth/verify-email/
    {
        "code": "123456"
    }
    """
    code = request.data.get('code')
    
    if not code:
        return Response({
            'error': 'Verification code is required'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        verification = VerificationCode.objects.get(
            userid=request.user,
            code=code,
            code_type='email',
            is_used=False
        )
        
        if not verification.is_valid():
            return Response({
                'error': 'Verification code has expired. Please request a new one.'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Mark as verified
        request.user.email_verified = True
        request.user.email_verified_at = timezone.now()
        
        # Check if fully verified
        if request.user.phone_verified:
            request.user.is_verified = True
        
        request.user.save()
        
        # Mark code as used
        verification.is_used = True
        verification.used_at = timezone.now()
        verification.save()
        
        return Response({
            'message': 'Email verified successfully',
            'email_verified': True,
            'is_fully_verified': request.user.is_verified
        }, status=status.HTTP_200_OK)
        
    except VerificationCode.DoesNotExist:
        return Response({
            'error': 'Invalid verification code'
        }, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def verify_phone_view(request):
    """
    Verify phone with code
    POST /api/auth/verify-phone/
    {
        "code": "654321"
    }
    """
    code = request.data.get('code')
    
    if not code:
        return Response({
            'error': 'Verification code is required'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        verification = VerificationCode.objects.get(
            userid=request.user,
            code=code,
            code_type='phone',
            is_used=False
        )
        
        if not verification.is_valid():
            return Response({
                'error': 'Verification code has expired. Please request a new one.'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Mark as verified
        request.user.phone_verified = True
        request.user.phone_verified_at = timezone.now()
        
        # Check if fully verified
        if request.user.email_verified:
            request.user.is_verified = True
        
        request.user.save()
        
        # Mark code as used
        verification.is_used = True
        verification.used_at = timezone.now()
        verification.save()
        
        # Notify if fully verified
        if request.user.is_verified:
            from notifications.utils import notify_verification_complete
            notify_verification_complete(request.user)
        
        return Response({
            'message': 'Phone verified successfully',
            'phone_verified': True,
            'is_fully_verified': request.user.is_verified
        }, status=status.HTTP_200_OK)
        
    except VerificationCode.DoesNotExist:
        return Response({
            'error': 'Invalid verification code'
        }, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def resend_code_view(request):
    """
    Resend verification code
    POST /api/auth/resend-code/
    {
        "code_type": "email"  # or "phone"
    }
    """
    code_type = request.data.get('code_type')
    
    if code_type not in ['email', 'phone']:
        return Response({
            'error': 'Invalid code type. Use "email" or "phone"'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    # Check if already verified
    if code_type == 'email' and request.user.email_verified:
        return Response({
            'error': 'Email already verified'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    if code_type == 'phone' and request.user.phone_verified:
        return Response({
            'error': 'Phone already verified'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    # Invalidate old codes
    VerificationCode.objects.filter(
        userid=request.user,
        code_type=code_type,
        is_used=False
    ).update(is_used=True)
    
    # Generate new code
    new_code = generate_code()
    contact_info = request.user.email if code_type == 'email' else request.user.phone_number
    expires_minutes = 15 if code_type == 'email' else 10
    
    VerificationCode.objects.create(
        userid=request.user,
        code=new_code,
        code_type=code_type,
        contact_info=contact_info,
        expires_at=timezone.now() + timedelta(minutes=expires_minutes)
    )
    
    # Send verification code
    from .utils import send_phone_verification_sms

    if code_type == 'phone':
        send_phone_verification_sms(request.user, new_code)
    else:
        # Email sending will be implemented later
        print(f"📧 Email verification code for {request.user.email}: {new_code}")

    return Response({
        'message': f'Verification code sent to your {code_type}',
        'code': new_code if settings.DEBUG else None  # Only include in DEBUG mode
    }, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def skip_verification_view(request):
    """
    Skip verification temporarily (user can verify later)
    POST /api/auth/skip-verification/
    """
    # User can use the platform but with limitations
    return Response({
        'message': 'You can verify your account later from your profile.',
        'user': UserProfileSerializer(request.user).data
    })


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def profile_view(request):
    """
    Get current user profile
    GET /api/auth/profile/
    """
    serializer = UserProfileSerializer(request.user)
    return Response(serializer.data)


@api_view(['PUT', 'PATCH'])
@permission_classes([IsAuthenticated])
def update_profile_view(request):
    """
    Update user profile
    PUT/PATCH /api/auth/profile/
    """
    serializer = UserProfileSerializer(
        request.user, 
        data=request.data, 
        partial=True
    )
    
    if serializer.is_valid():
        serializer.save()
        return Response({
            'message': 'Profile updated successfully',
            'user': serializer.data
        })
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_email_view(request):
    """
    Update email and send new verification code
    PUT /api/auth/update-email/
    {
        "email": "newemail@example.com"
    }
    """
    new_email = request.data.get('email')
    
    if not new_email:
        return Response({
            'error': 'Email is required'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    # Check if email already exists
    if User.objects.filter(email=new_email).exclude(userid=request.user.userid).exists():
        return Response({
            'error': 'This email is already registered'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    # Update email
    request.user.email = new_email
    request.user.email_verified = False
    request.user.email_verified_at = None
    request.user.save()
    
    # Invalidate old codes
    VerificationCode.objects.filter(
        userid=request.user,
        code_type='email',
        is_used=False
    ).update(is_used=True)
    
    # Generate new code
    email_code = generate_code()
    VerificationCode.objects.create(
        userid=request.user,
        code=email_code,
        code_type='email',
        contact_info=new_email,
        expires_at=timezone.now() + timedelta(minutes=15)
    )
    
    print(f"📧 New email verification code for {new_email}: {email_code}")
    
    return Response({
        'message': 'Email updated. Verification code sent.',
        'email': new_email,
        'code': email_code if settings.DEBUG else None
    })


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_phone_view(request):
    """
    Update phone and send new verification code
    PUT /api/auth/update-phone/
    {
        "phone_number": "+25779999999"
    }
    """
    new_phone = request.data.get('phone_number')
    
    if not new_phone:
        return Response({
            'error': 'Phone number is required'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    # Validate phone format
    import re
    if not re.match(r'^\+257[0-9]{8}$', new_phone):
        return Response({
            'error': 'Phone must start with +257 and have 8 digits'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    # Update phone
    request.user.phone_number = new_phone
    request.user.phone_verified = False
    request.user.phone_verified_at = None
    request.user.save()
    
    # Invalidate old codes
    VerificationCode.objects.filter(
        userid=request.user,
        code_type='phone',
        is_used=False
    ).update(is_used=True)
    
    # Generate new code
    phone_code = generate_code()
    VerificationCode.objects.create(
        userid=request.user,
        code=phone_code,
        code_type='phone',
        contact_info=new_phone,
        expires_at=timezone.now() + timedelta(minutes=10)
    )
    
    print(f"📱 New phone verification code for {new_phone}: {phone_code}")
    
    return Response({
        'message': 'Phone updated. Verification code sent.',
        'phone_number': new_phone,
        'code': phone_code if settings.DEBUG else None
    })

