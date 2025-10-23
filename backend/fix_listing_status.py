#!/usr/bin/env python
"""
Script to check and update listing statuses to 'active' for testing
Run this with: python manage.py shell < fix_listing_status.py
"""

import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'umuhuza.settings')
django.setup()

from listings.models import Listing

print("\n" + "="*60)
print("LISTING STATUS CHECKER AND FIXER")
print("="*60 + "\n")

# Get all listings
listings = Listing.objects.all()

if not listings.exists():
    print("❌ No listings found in database!")
    print("   Create a listing first, then run this script.\n")
else:
    print(f"Found {listings.count()} listing(s):\n")

    for listing in listings:
        print(f"📋 Listing #{listing.listing_id}: {listing.listing_title}")
        print(f"   Status: {listing.listing_status}")
        print(f"   Featured: {listing.is_featured}")
        print(f"   Owner: {listing.userid.email}")

        # Check if star button would show
        can_promote = not listing.is_featured and listing.listing_status == 'active'

        if can_promote:
            print(f"   ⭐ Star button: VISIBLE ✅")
        else:
            print(f"   ⭐ Star button: HIDDEN ❌")
            if listing.is_featured:
                print(f"      Reason: Already featured")
            if listing.listing_status != 'active':
                print(f"      Reason: Status is '{listing.listing_status}' (needs to be 'active')")

        print()

    # Ask to fix
    print("\n" + "-"*60)
    pending_listings = listings.filter(listing_status='pending')

    if pending_listings.exists():
        print(f"\n⚠️  Found {pending_listings.count()} listing(s) with 'pending' status")
        print("   These won't show the star button until status is 'active'\n")

        # Auto-fix for development
        print("🔧 Updating all pending listings to 'active'...")
        updated = pending_listings.update(listing_status='active')
        print(f"✅ Updated {updated} listing(s) to 'active' status\n")

        print("Updated listings:")
        for listing in Listing.objects.all():
            can_promote = not listing.is_featured and listing.listing_status == 'active'
            status_icon = "✅" if can_promote else "❌"
            print(f"   {status_icon} #{listing.listing_id}: {listing.listing_title} - {listing.listing_status}")
    else:
        print("✅ All listings are already active!\n")

print("\n" + "="*60)
print("DONE! Refresh your browser to see the star buttons.")
print("="*60 + "\n")
