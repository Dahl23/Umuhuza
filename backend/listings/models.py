from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
import uuid

from users.models import User

# ============================================================================
# CATEGORIES
# ============================================================================

class Category(models.Model):
    cat_id = models.AutoField(primary_key=True, db_column='CAT_ID')
    cat_name = models.CharField(max_length=255, db_column='CAT_NAME', default='Uncategorized')
    slug = models.SlugField(max_length=255, unique=True, db_column='SLUG')
    cat_description = models.TextField(db_column='CAT_DESCRIPTION', default='Category description')
    is_active = models.BooleanField(default=True, db_column='IS_ACTIVE')
    createdat = models.DateTimeField(auto_now_add=True, db_column='CREATEDAT')
    updatedat = models.DateTimeField(auto_now=True, db_column='UPDATEDAT')
    
    class Meta:
        db_table = 'CATEGORIES'
        verbose_name_plural = 'Categories'
    
    def __str__(self):
        return self.cat_name


# ============================================================================
# PRICING PLANS
# ============================================================================

class PricingPlan(models.Model):
    CATEGORY_SCOPE = [
        ('all', 'All Categories'),
        ('real_estate', 'Real Estate'),
        ('vehicle', 'Vehicle'),
    ]
    
    pricing_id = models.AutoField(primary_key=True, db_column='PRICING_ID')
    pricing_name = models.CharField(max_length=255, db_column='PRICING_NAME')
    pricing_description = models.TextField(db_column='PRICING_DESCRIPTION')
    plan_price = models.DecimalField(max_digits=12, decimal_places=2, db_column='PLAN_PRICE')
    duration_days = models.IntegerField(db_column='DURATION_DAYS')
    category_scope = models.CharField(max_length=20, choices=CATEGORY_SCOPE, db_column='CATEGORY_SCOPE')
    max_listings = models.IntegerField(default=1, db_column='MAX_LISTINGS')
    max_images_per_listing = models.IntegerField(default=5, db_column='MAX_IMAGES_PER_LISTING')
    is_featured = models.BooleanField(default=False, db_column='IS_FEATURED')
    is_active = models.BooleanField(default=True, db_column='IS_ACTIVE')
    createdat = models.DateTimeField(auto_now_add=True, db_column='CREATEDAT')
    updatedat = models.DateTimeField(auto_now=True, db_column='UPDATEDAT')
    
    class Meta:
        db_table = 'PRICING_PLANS'
    
    def __str__(self):
        return f"{self.pricing_name} - {self.plan_price} BIF"


# ============================================================================
# USER SUBSCRIPTIONS
# ============================================================================

class UserSubscription(models.Model):
    SUBSCRIPTION_STATUS = [
        ('active', 'Active'),
        ('expired', 'Expired'),
        ('cancelled', 'Cancelled'),
    ]

    subscription_id = models.AutoField(primary_key=True, db_column='SUBSCRIPTION_ID')
    userid = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        db_column='USERID',
        related_name='subscriptions'
    )
    pricing_id = models.ForeignKey(
        PricingPlan,
        on_delete=models.RESTRICT,
        db_column='PRICING_ID'
    )
    subscription_status = models.CharField(
        max_length=10,
        choices=SUBSCRIPTION_STATUS,
        default='active',
        db_column='SUBSCRIPTION_STATUS'
    )
    listings_used = models.IntegerField(default=0, db_column='LISTINGS_USED')
    starts_at = models.DateTimeField(db_column='STARTS_AT')
    expires_at = models.DateTimeField(null=True, blank=True, db_column='EXPIRES_AT')
    auto_renew = models.BooleanField(default=False, db_column='AUTO_RENEW')
    createdat = models.DateTimeField(auto_now_add=True, db_column='CREATEDAT')
    updatedat = models.DateTimeField(auto_now=True, db_column='UPDATEDAT')

    class Meta:
        db_table = 'USER_SUBSCRIPTIONS'
        indexes = [
            models.Index(fields=['userid']),
            models.Index(fields=['subscription_status']),
            models.Index(fields=['expires_at']),
        ]

    def __str__(self):
        return f"{self.userid.full_name} - {self.pricing_id.pricing_name}"

    @property
    def is_active(self):
        """Check if subscription is currently active"""
        if self.subscription_status != 'active':
            return False
        if self.expires_at and self.expires_at < timezone.now():
            return False
        return True

    @property
    def remaining_listings(self):
        """Calculate remaining listings quota"""
        return max(0, self.pricing_id.max_listings - self.listings_used)

    @property
    def has_quota(self):
        """Check if user still has listing quota available"""
        return self.remaining_listings > 0


# ============================================================================
# LISTINGS
# ============================================================================

class Listing(models.Model):
    LISTING_STATUS = [
        ('active', 'Active'),
        ('pending', 'Pending'),
        ('sold', 'Sold'),
        ('expired', 'Expired'),
        ('hidden', 'Hidden'),
    ]
    
    listing_id = models.AutoField(primary_key=True, db_column='LISTING_ID')
    userid = models.ForeignKey(User, on_delete=models.CASCADE, db_column='USERID', related_name='listings')
    cat_id = models.ForeignKey(Category, on_delete=models.RESTRICT, db_column='CAT_ID')
    listing_title = models.CharField(max_length=255, db_column='LISTING_TITLE')
    list_description = models.TextField(db_column='LIST_DESCRIPTION')
    listing_price = models.DecimalField(max_digits=15, decimal_places=2, db_column='LISTING_PRICE')
    list_location = models.CharField(max_length=255, db_column='LIST_LOCATION')
    listing_status = models.CharField(
        max_length=10, 
        choices=LISTING_STATUS, 
        default='pending',
        db_column='LISTING_STATUS'
    )
    views = models.IntegerField(default=0, db_column='VIEWS')
    is_featured = models.BooleanField(default=False, db_column='IS_FEATURED')
    expiration_date = models.DateTimeField(null=True, blank=True, db_column='EXPIRATION_DATE')
    createdat = models.DateTimeField(auto_now_add=True, db_column='CREATEDAT')
    updatedat = models.DateTimeField(auto_now=True, db_column='UPDATEDAT')
    
    class Meta:
        db_table = 'LISTINGS'
        indexes = [
            models.Index(fields=['userid']),
            models.Index(fields=['cat_id']),
            models.Index(fields=['listing_status']),
            models.Index(fields=['is_featured']),
            models.Index(fields=['list_location']),
            models.Index(fields=['listing_price']),
            models.Index(fields=['createdat']),
        ]
        ordering = ['-createdat']
    
    def __str__(self):
        return self.listing_title
    
    def increment_views(self):
        self.views += 1
        self.save(update_fields=['views'])


# ============================================================================
# LISTING IMAGES
# ============================================================================

class ListingImage(models.Model):
    listimage_id = models.AutoField(primary_key=True, db_column='LISTIMAGE_ID')
    listing_id = models.ForeignKey(
        Listing, 
        on_delete=models.CASCADE, 
        db_column='LISTING_ID',
        related_name='images'
    )
    image_url = models.CharField(max_length=255, db_column='IMAGE_URL')
    is_primary = models.BooleanField(default=False, db_column='IS_PRIMARY')
    display_order = models.IntegerField(default=0, db_column='DISPLAY_ORDER')
    uploadedat = models.DateTimeField(auto_now_add=True, db_column='UPLOADEDAT')
    
    class Meta:
        db_table = 'LISTING_IMAGES'
        ordering = ['display_order']
    
    def __str__(self):
        return f"Image for {self.listing_id.listing_title}"


# ============================================================================
# RATINGS & REVIEWS
# ============================================================================

class RatingReview(models.Model):
    ratingrev_id = models.AutoField(primary_key=True, db_column='RATINGREV_ID')
    userid = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        db_column='USERID',
        related_name='reviews_given'
    )
    reviewed_userid = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        db_column='REVIEWED_USERID',
        related_name='reviews_received'
    )
    listing_id = models.ForeignKey(
        Listing, 
        on_delete=models.CASCADE, 
        null=True, 
        blank=True,
        db_column='LISTING_ID'
    )
    rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        db_column='RATING'
    )
    comment = models.TextField(null=True, blank=True, db_column='COMMENT')
    is_visible = models.BooleanField(default=True, db_column='IS_VISIBLE')
    createdat = models.DateTimeField(auto_now_add=True, db_column='CREATEDAT')
    updatedat = models.DateTimeField(auto_now=True, db_column='UPDATEDAT')
    
    class Meta:
        db_table = 'RATINGS_N_REVIEWS'
        unique_together = [['userid', 'reviewed_userid', 'listing_id']]
        indexes = [
            models.Index(fields=['reviewed_userid']),
            models.Index(fields=['rating']),
        ]
    
    def __str__(self):
        return f"{self.userid.full_name} rated {self.reviewed_userid.full_name} - {self.rating}/5"


# ============================================================================
# FAVORITES
# ============================================================================

class Favorite(models.Model):
    fav_id = models.AutoField(primary_key=True, db_column='FAV_ID')
    userid = models.ForeignKey(User, on_delete=models.CASCADE, db_column='USERID')
    listing_id = models.ForeignKey(Listing, on_delete=models.CASCADE, db_column='LISTING_ID')
    createdat = models.DateTimeField(auto_now_add=True, db_column='CREATEDAT')
    
    class Meta:
        db_table = 'FAVORITES'
        unique_together = [['userid', 'listing_id']]
    
    def __str__(self):
        return f"{self.userid.full_name} favorited {self.listing_id.listing_title}"


# ============================================================================
# REPORTS & MISCONDUCT
# ============================================================================

class ReportMisconduct(models.Model):
    REPORT_TYPES = [
        ('spam', 'Spam'),
        ('fraud', 'Fraud'),
        ('inappropriate', 'Inappropriate'),
        ('duplicate', 'Duplicate'),
        ('harassment', 'Harassment'),
        ('other', 'Other'),
    ]
    
    REPORT_STATUS = [
        ('pending', 'Pending'),
        ('resolved', 'Resolved'),
        ('rejected', 'Rejected'),
    ]
    
    reportmiscond_id = models.AutoField(primary_key=True, db_column='REPORTMISCOND_ID')
    userid = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        db_column='USERID',
        related_name='reports_submitted'
    )
    reported_userid = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        db_column='REPORTED_USERID',
        related_name='reports_received'
    )
    listing_id = models.ForeignKey(
        Listing, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        db_column='LISTING_ID'
    )
    report_reason = models.TextField(db_column='REPORT_REASON')
    report_type = models.CharField(max_length=20, choices=REPORT_TYPES, db_column='REPORT_TYPE')
    report_status = models.CharField(
        max_length=10, 
        choices=REPORT_STATUS, 
        default='pending',
        db_column='REPORT_STATUS'
    )
    admin_notes = models.TextField(null=True, blank=True, db_column='ADMIN_NOTES')
    createdat = models.DateTimeField(auto_now_add=True, db_column='CREATEDAT')
    resolved_at = models.DateTimeField(null=True, blank=True, db_column='RESOLVED_AT')
    
    class Meta:
        db_table = 'REPORTS_N_MISCONDUCT'
        indexes = [
            models.Index(fields=['userid']),
            models.Index(fields=['reported_userid']),
            models.Index(fields=['listing_id']),
            models.Index(fields=['report_status']),
        ]
    
    def __str__(self):
        return f"Report by {self.userid.full_name} - {self.report_type}"

