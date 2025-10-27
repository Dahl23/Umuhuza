from django.urls import path
from . import views

urlpatterns = [
    # Categories
    path('categories/', views.category_list, name='category-list'),
    path('categories/<int:pk>/', views.category_detail, name='category-detail'),
    
    # Listings
    path('listings/', views.ListingListView.as_view(), name='listing-list'),
    path('listings/create/', views.listing_create, name='listing-create'),
    path('listings/my-listings/', views.my_listings, name='my-listings'),
    path('listings/featured/', views.featured_listings, name='featured-listings'),
    path('listings/<int:pk>/', views.listing_detail, name='listing-detail'),
    path('listings/<int:pk>/update/', views.listing_update, name='listing-update'),
    path('listings/<int:pk>/update-status/', views.listing_update_status, name='listing-update-status'),
    path('listings/<int:pk>/delete/', views.listing_delete, name='listing-delete'),
    path('listings/<int:pk>/similar/', views.similar_listings, name='similar-listings'),
    
    # Favorites
    path('favorites/', views.favorite_list, name='favorite-list'),
    path('favorites/<int:listing_id>/toggle/', views.favorite_toggle, name='favorite-toggle'),
    
    # Reviews
    path('reviews/user/<int:user_id>/', views.review_list, name='review-list'),
    path('reviews/create/', views.review_create, name='review-create'),
    
    # Pricing Plans
    path('pricing-plans/', views.pricing_plans_list, name='pricing-plans'),

    # User Subscription
    path('subscription/current/', views.current_subscription, name='current-subscription'),
    
    # Reports
    path('reports/create/', views.report_create, name='report-create'),
    path('reports/my-reports/', views.my_reports, name='my-reports'),
    path('reports/<int:pk>/', views.report_detail, name='report-detail'),
    
    # Images
    path('listings/<int:listing_id>/upload-image/', views.upload_listing_image, name='upload-image'),
    path('listings/<int:listing_id>/images/<int:image_id>/', views.delete_listing_image, name='delete-image'),
    path('listings/<int:listing_id>/images/<int:image_id>/set-primary/', views.set_primary_image, name='set-primary-image'),

]