from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.utils import timezone
from datetime import timedelta
import uuid

from .models import Payment, DealerApplication, DealerDocument
from .serializers import (
    PaymentSerializer, PaymentCreateSerializer,
    DealerApplicationSerializer, DealerDocumentSerializer
)
from listings.models import PricingPlan, Listing, UserSubscription
from notifications.utils import notify_payment_success, create_notification


# ============================================================================
# DEALER APPLICATIONS
# ============================================================================

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def dealer_application_create(request):
    """
    Submit dealer application
    POST /api/dealer-applications/create/
    {
        "business_name": "Premium Real Estate",
        "business_type": "real_estate",
        "business_address": "123 Main St, Bujumbura",
        "business_phone": "+25779111222",
        "business_email": "contact@premiumre.bi",
        "tax_id": "TIN123456789"
    }
    """
    # Check if user already has an application
    if DealerApplication.objects.filter(userid=request.user).exists():
        return Response({
            'error': 'You already have a dealer application'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    serializer = DealerApplicationSerializer(data=request.data)
    
    if serializer.is_valid():
        application = serializer.save(userid=request.user)
        
        create_notification(
            user=request.user,
            title='Application Submitted',
            message='Your dealer application has been submitted and is under review',
            notif_type='system'
        )
        
        return Response({
            'message': 'Dealer application submitted successfully',
            'application': DealerApplicationSerializer(application).data
        }, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def dealer_application_status(request):
    """
    Get user's dealer application status
    GET /api/dealer-applications/status/
    """
    try:
        application = DealerApplication.objects.get(userid=request.user)
        serializer = DealerApplicationSerializer(application)
        return Response(serializer.data)
    except DealerApplication.DoesNotExist:
        return Response({
            'message': 'No dealer application found',
            'has_application': False
        })


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def dealer_document_upload(request):
    """
    Upload dealer documents (placeholder - actual file upload later)
    POST /api/dealer-applications/documents/
    {
        "doc_type": "business_license",
        "file_url": "path/to/file.pdf"
    }
    """
    try:
        application = DealerApplication.objects.get(userid=request.user)
    except DealerApplication.DoesNotExist:
        return Response({
            'error': 'No dealer application found'
        }, status=status.HTTP_404_NOT_FOUND)
    
    doc_type = request.data.get('doc_type')
    file_url = request.data.get('file_url')  # Will be actual file upload later
    
    if not doc_type or not file_url:
        return Response({
            'error': 'doc_type and file_url are required'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    document = DealerDocument.objects.create(
        dealerapp_id=application,
        doc_type=doc_type,
        file_url=file_url
    )
    
    return Response({
        'message': 'Document uploaded successfully',
        'document': DealerDocumentSerializer(document).data
    }, status=status.HTTP_201_CREATED)


# ============================================================================
# PAYMENTS
# ============================================================================

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def payment_initiate(request):
    """
    Initiate payment for pricing plan
    POST /api/payments/initiate/
    {
        "pricing_id": 1,
        "listing_id": 5,  // Optional
        "payment_method": "mobile_money",
        "phone_number": "+25779123456"  // For mobile money
    }
    """
    serializer = PaymentCreateSerializer(data=request.data)
    
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    pricing_id = serializer.validated_data['pricing_id']
    listing_id = serializer.validated_data.get('listing_id')
    payment_method = serializer.validated_data['payment_method']
    phone_number = serializer.validated_data.get('phone_number')
    
    # Get pricing plan
    pricing_plan = get_object_or_404(PricingPlan, pk=pricing_id, is_active=True)
    
    # Validate listing if provided
    listing = None
    if listing_id:
        listing = get_object_or_404(Listing, pk=listing_id, userid=request.user)
    
    # Generate payment IDs
    payment_id = str(uuid.uuid4())
    payment_ref = f"UMH-{uuid.uuid4().hex[:10].upper()}"
    
    # Create payment record
    payment = Payment.objects.create(
        payment_id=payment_id,
        userid=request.user,
        pricing_id=pricing_plan,
        listing_id=listing,
        payment_amount=pricing_plan.plan_price,
        payment_method=payment_method,
        payment_ref=payment_ref,
        payment_status='pending'
    )
    
    # TODO: Integrate with actual payment gateway (Lumicash/Flutterwave)
    # For now, simulate payment
    if payment_method == 'mobile_money':
        # In production, call Lumicash API here
        response_data = {
            'payment_id': payment_id,
            'payment_ref': payment_ref,
            'amount': float(pricing_plan.plan_price),
            'message': 'Check your phone for payment prompt',
            'status': 'pending'
        }
    else:
        response_data = {
            'payment_id': payment_id,
            'payment_ref': payment_ref,
            'amount': float(pricing_plan.plan_price),
            'message': 'Payment initiated',
            'status': 'pending'
        }
    
    return Response(response_data, status=status.HTTP_201_CREATED)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def payment_verify(request):
    """
    Verify/confirm payment (for testing - in production, webhook from gateway)
    POST /api/payments/verify/
    {
        "payment_ref": "UMH-ABC123XYZ"
    }
    """
    payment_ref = request.data.get('payment_ref')
    
    if not payment_ref:
        return Response({
            'error': 'payment_ref is required'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        payment = Payment.objects.get(payment_ref=payment_ref, userid=request.user)
    except Payment.DoesNotExist:
        return Response({
            'error': 'Payment not found'
        }, status=status.HTTP_404_NOT_FOUND)
    
    if payment.payment_status == 'successful':
        return Response({
            'message': 'Payment already confirmed'
        })
    
    # Simulate successful payment (in production, verify with gateway)
    payment.payment_status = 'successful'
    payment.confirmed_at = timezone.now()
    payment.transaction_id = f"TXN-{uuid.uuid4().hex[:12].upper()}"
    payment.save()

    plan = payment.pricing_id

    # Create or update user subscription
    starts_at = timezone.now()
    expires_at = starts_at + timedelta(days=plan.duration_days)

    # Check if user already has an active subscription for this plan
    subscription = UserSubscription.objects.filter(
        userid=request.user,
        pricing_id=plan,
        subscription_status='active'
    ).first()

    if subscription:
        # Extend existing subscription
        if subscription.expires_at and subscription.expires_at > timezone.now():
            # Add to existing expiration
            subscription.expires_at = subscription.expires_at + timedelta(days=plan.duration_days)
        else:
            # Renew from now
            subscription.starts_at = starts_at
            subscription.expires_at = expires_at
        subscription.subscription_status = 'active'
        subscription.save()
    else:
        # Create new subscription
        subscription = UserSubscription.objects.create(
            userid=request.user,
            pricing_id=plan,
            subscription_status='active',
            starts_at=starts_at,
            expires_at=expires_at,
            listings_used=0,
            auto_renew=False
        )

    # Apply benefits to specific listing if provided
    if payment.listing_id:
        listing = payment.listing_id

        if plan.is_featured:
            listing.is_featured = True

        listing.expiration_date = expires_at
        listing.listing_status = 'active'
        listing.save()

        # Increment subscription's listing counter
        subscription.listings_used += 1
        subscription.save(update_fields=['listings_used', 'updatedat'])

    # Notify user
    notify_payment_success(
        user=request.user,
        amount=payment.payment_amount,
        plan_name=payment.pricing_id.pricing_name
    )
    
    return Response({
        'message': 'Payment verified successfully',
        'payment': PaymentSerializer(payment).data
    })


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def payment_history(request):
    """
    Get user's payment history
    GET /api/payments/history/
    """
    payments = Payment.objects.filter(
        userid=request.user
    ).select_related('pricing_id', 'listing_id').order_by('-createdat')
    
    serializer = PaymentSerializer(payments, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def payment_detail(request, payment_id):
    """
    Get payment details
    GET /api/payments/{payment_id}/
    """
    payment = get_object_or_404(Payment, payment_id=payment_id, userid=request.user)
    serializer = PaymentSerializer(payment)
    return Response(serializer.data)