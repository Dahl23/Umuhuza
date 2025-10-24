
from rest_framework import serializers
from django.contrib.auth import get_user_model

from users.serializers import UserPublicSerializer
from .models import (
    User, Category, Listing, ListingImage,
    PricingPlan, RatingReview, Favorite, ReportMisconduct, UserSubscription
)

User = get_user_model()
# ============================================================================
# CATEGORY SERIALIZERS
# ============================================================================

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['cat_id', 'cat_name', 'slug', 'cat_description']


# ============================================================================
# LISTING SERIALIZERS
# ============================================================================

class ListingImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ListingImage
        fields = ['listimage_id', 'image_url', 'is_primary', 'display_order']


class ListingSerializer(serializers.ModelSerializer):
    images = ListingImageSerializer(many=True, read_only=True)
    category = CategorySerializer(source='cat_id', read_only=True)
    seller = UserPublicSerializer(source='userid', read_only=True)
    
    class Meta:
        model = Listing
        fields = [
            'listing_id', 'listing_title', 'list_description', 
            'listing_price', 'list_location', 'listing_status',
            'views', 'is_featured', 'expiration_date', 
            'createdat', 'updatedat', 'images', 'category', 'seller'
        ]
        read_only_fields = ['listing_id', 'views', 'createdat', 'updatedat']


class ListingCreateSerializer(serializers.ModelSerializer):
    images = serializers.ListField(
        child=serializers.ImageField(),
        write_only=True,
        required=False
    )
    
    class Meta:
        model = Listing
        fields = [
            'cat_id', 'listing_title', 'list_description',
            'listing_price', 'list_location', 'images'
        ]
    
    def create(self, validated_data):
        images_data = validated_data.pop('images', [])
        listing = Listing.objects.create(**validated_data)
        
        # Handle image uploads here (you'll need to implement file upload logic)
        for idx, image in enumerate(images_data):
            ListingImage.objects.create(
                listing_id=listing,
                image_url=f"uploads/listings/{listing.listing_id}/{image.name}",
                is_primary=(idx == 0),
                display_order=idx
            )
        
        return listing


class ListingDetailSerializer(serializers.ModelSerializer):
    images = ListingImageSerializer(many=True, read_only=True)
    category = CategorySerializer(source='cat_id', read_only=True)
    seller = UserPublicSerializer(source='userid', read_only=True)
    is_favorited = serializers.SerializerMethodField()
    
    class Meta:
        model = Listing
        fields = [
            'listing_id', 'listing_title', 'list_description', 
            'listing_price', 'list_location', 'listing_status',
            'views', 'is_featured', 'expiration_date', 
            'createdat', 'updatedat', 'images', 'category', 
            'seller', 'is_favorited'
        ]
    
    def get_is_favorited(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return Favorite.objects.filter(
                userid=request.user, 
                listing_id=obj
            ).exists()
        return False


# ============================================================================
# PRICING PLAN SERIALIZERS
# ============================================================================

class PricingPlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = PricingPlan
        fields = [
            'pricing_id', 'pricing_name', 'pricing_description',
            'plan_price', 'duration_days', 'category_scope',
            'max_listings', 'max_images_per_listing', 'is_featured'
        ]


class UserSubscriptionSerializer(serializers.ModelSerializer):
    plan = PricingPlanSerializer(source='pricing_id', read_only=True)
    is_active = serializers.BooleanField(read_only=True)
    remaining_listings = serializers.IntegerField(read_only=True)
    has_quota = serializers.BooleanField(read_only=True)

    class Meta:
        model = UserSubscription
        fields = [
            'subscription_id', 'plan', 'subscription_status',
            'listings_used', 'starts_at', 'expires_at',
            'is_active', 'remaining_listings', 'has_quota',
            'createdat', 'updatedat'
        ]
        read_only_fields = [
            'subscription_id', 'createdat', 'updatedat'
        ]


# ============================================================================
# RATING & REVIEW SERIALIZERS
# ============================================================================

class RatingReviewSerializer(serializers.ModelSerializer):
    reviewer = UserPublicSerializer(source='userid', read_only=True)
    
    class Meta:
        model = RatingReview
        fields = [
            'ratingrev_id', 'reviewer', 'rating', 'comment',
            'createdat', 'updatedat'
        ]
        read_only_fields = ['ratingrev_id', 'createdat', 'updatedat']


class RatingReviewCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = RatingReview
        fields = ['reviewed_userid', 'listing_id', 'rating', 'comment']
    
    def validate_rating(self, value):
        if not 1 <= value <= 5:
            raise serializers.ValidationError("Rating must be between 1 and 5")
        return value
    
# ============================================================================
# FAVORITE SERIALIZERS
# ============================================================================

class FavoriteSerializer(serializers.ModelSerializer):
    listing = ListingSerializer(source='listing_id', read_only=True)
    
    class Meta:
        model = Favorite
        fields = ['fav_id', 'listing', 'createdat']
        read_only_fields = ['fav_id', 'createdat']


class ReportMisconductSerializer(serializers.ModelSerializer):
    reporter = UserPublicSerializer(source='userid', read_only=True)
    reported_user = UserPublicSerializer(source='reported_userid', read_only=True)
    
    class Meta:
        model = ReportMisconduct
        fields = [
            'reportmiscond_id', 'reporter', 'reported_user', 'listing_id',
            'report_reason', 'report_type', 'report_status', 'createdat'
        ]
        read_only_fields = ['reportmiscond_id', 'report_status', 'createdat']


class ReportCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReportMisconduct
        fields = ['reported_userid', 'listing_id', 'report_type', 'report_reason']
    
    def validate(self, data):
        # Must report either a user or a listing
        if not data.get('reported_userid') and not data.get('listing_id'):
            raise serializers.ValidationError(
                "You must report either a user or a listing"
            )
        return data