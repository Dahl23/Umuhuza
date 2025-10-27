from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import (
    Payment,
    DealerApplication, DealerDocument
)
from listings.models import PricingPlan

User = get_user_model()

# ============================================================================
# PAYMENT SERIALIZERS
# ============================================================================

class PricingPlanNestedSerializer(serializers.ModelSerializer):
    """Nested serializer for pricing plan in payment responses"""
    class Meta:
        model = PricingPlan
        fields = ['pricing_id', 'pricing_name', 'pricing_description', 'plan_price', 'duration_days']


class PaymentSerializer(serializers.ModelSerializer):
    pricing_id = PricingPlanNestedSerializer(read_only=True)

    class Meta:
        model = Payment
        fields = [
            'payment_id', 'userid', 'pricing_id', 'listing_id',
            'payment_amount', 'payment_method', 'payment_status',
            'payment_ref', 'transaction_id', 'createdat', 'confirmed_at'
        ]
        read_only_fields = ['payment_id', 'payment_status', 'createdat', 'confirmed_at']


class PaymentCreateSerializer(serializers.Serializer):
    pricing_id = serializers.IntegerField()
    listing_id = serializers.IntegerField(required=False)
    payment_method = serializers.ChoiceField(choices=['mobile_money', 'card', 'wallet'])
    phone_number = serializers.CharField(max_length=20, required=False)

# ============================================================================
# DEALER APPLICATION SERIALIZERS
# ============================================================================

class DealerDocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = DealerDocument
        fields = ['dealerdoc_id', 'doc_type', 'file_url', 'verified', 'uploadedat']


class DealerApplicationSerializer(serializers.ModelSerializer):
    documents = DealerDocumentSerializer(many=True, read_only=True)
    
    class Meta:
        model = DealerApplication
        fields = [
            'dealerapp_id', 'business_name', 'business_type',
            'business_address', 'business_phone', 'business_email',
            'tax_id', 'business_license', 'appli_status',
            'rejection_reason', 'createdat', 'approvedat', 'documents'
        ]
        read_only_fields = [
            'dealerapp_id', 'appli_status', 'rejection_reason',
            'createdat', 'approvedat'
        ]

