"""
Django management command to set up the Umuhuza platform database with initial data.

Usage:
    python manage.py setup_database [--reset]

This command creates:
- Predefined categories for real estate and vehicles
- Default pricing plans (Basic, Premium, Dealer)
- Sample admin user (for development only)

Options:
    --reset: Delete existing data before creating new records (WARNING: destructive)
"""

from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth import get_user_model
from listings.models import Category, PricingPlan
from decimal import Decimal

User = get_user_model()


class Command(BaseCommand):
    help = 'Set up the Umuhuza platform database with initial categories and pricing plans'

    def add_arguments(self, parser):
        parser.add_argument(
            '--reset',
            action='store_true',
            help='Delete existing categories and pricing plans before creating new ones (WARNING: destructive)',
        )

    def handle(self, *args, **options):
        reset = options.get('reset', False)

        self.stdout.write(self.style.SUCCESS('\n' + '=' * 70))
        self.stdout.write(self.style.SUCCESS('🚀 UMUHUZA PLATFORM - DATABASE SETUP'))
        self.stdout.write(self.style.SUCCESS('=' * 70 + '\n'))

        if reset:
            self.stdout.write(self.style.WARNING('⚠️  RESET MODE: Deleting existing data...\n'))
            self.delete_existing_data()

        # Create categories
        self.stdout.write(self.style.HTTP_INFO('📁 Setting up categories...'))
        categories_created = self.create_categories()

        # Create pricing plans
        self.stdout.write(self.style.HTTP_INFO('\n💰 Setting up pricing plans...'))
        plans_created = self.create_pricing_plans()

        # Summary
        self.stdout.write(self.style.SUCCESS('\n' + '=' * 70))
        self.stdout.write(self.style.SUCCESS('✅ DATABASE SETUP COMPLETE'))
        self.stdout.write(self.style.SUCCESS('=' * 70))
        self.stdout.write(f'\n📊 Summary:')
        self.stdout.write(f'  • Categories: {categories_created} created')
        self.stdout.write(f'  • Pricing Plans: {plans_created} created')
        self.stdout.write(self.style.SUCCESS('\n✨ Your platform is ready to use!\n'))

    def delete_existing_data(self):
        """Delete existing categories and pricing plans"""
        try:
            categories_count = Category.objects.all().count()
            plans_count = PricingPlan.objects.all().count()

            Category.objects.all().delete()
            PricingPlan.objects.all().delete()

            self.stdout.write(self.style.WARNING(f'  ✓ Deleted {categories_count} categories'))
            self.stdout.write(self.style.WARNING(f'  ✓ Deleted {plans_count} pricing plans'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'  ✗ Error during deletion: {str(e)}'))

    def create_categories(self):
        """Create predefined listing categories"""
        from django.utils.text import slugify

        categories = [
            {
                'cat_name': 'Houses & Apartments',
                'cat_description': 'Residential properties including houses, apartments, villas, and townhouses for sale or rent'
            },
            {
                'cat_name': 'Land & Plots',
                'cat_description': 'Residential and commercial land, plots, and empty lots for sale'
            },
            {
                'cat_name': 'Commercial Properties',
                'cat_description': 'Office spaces, shops, warehouses, and commercial buildings'
            },
            {
                'cat_name': 'Cars',
                'cat_description': 'New and used cars, sedans, SUVs, and passenger vehicles'
            },
            {
                'cat_name': 'Trucks & Commercial Vehicles',
                'cat_description': 'Pickup trucks, delivery vans, lorries, and commercial vehicles'
            },
            {
                'cat_name': 'Motorcycles & Bikes',
                'cat_description': 'Motorcycles, scooters, and bicycles'
            },
            {
                'cat_name': 'Buses & Minibuses',
                'cat_description': 'Passenger buses, minibuses, and shuttle vehicles'
            },
            {
                'cat_name': 'Heavy Equipment',
                'cat_description': 'Construction equipment, tractors, and industrial vehicles'
            },
        ]

        created_count = 0
        for cat_data in categories:
            slug = slugify(cat_data['cat_name'])
            category, created = Category.objects.get_or_create(
                slug=slug,
                defaults={
                    'cat_name': cat_data['cat_name'],
                    'cat_description': cat_data['cat_description'],
                    'is_active': True
                }
            )
            if created:
                created_count += 1
                self.stdout.write(f'  ✓ Created: {category.cat_name}')
            else:
                self.stdout.write(f'  ⊙ Exists: {category.cat_name}')

        return created_count

    def create_pricing_plans(self):
        """Create predefined pricing plans"""
        plans = [
            {
                'pricing_name': 'Basic Plan',
                'pricing_description': 'Perfect for individual sellers listing a single property or vehicle',
                'plan_price': Decimal('0.00'),
                'duration_days': 30,
                'category_scope': 'all',
                'max_listings': 1,
                'max_images_per_listing': 5,
                'is_featured': False
            },
            {
                'pricing_name': 'Premium Plan',
                'pricing_description': 'Ideal for sellers with multiple listings and better visibility',
                'plan_price': Decimal('50000.00'),  # 50,000 BIF
                'duration_days': 30,
                'category_scope': 'all',
                'max_listings': 10,
                'max_images_per_listing': 10,
                'is_featured': False
            },
            {
                'pricing_name': 'Dealer Monthly',
                'pricing_description': 'Unlimited listings for professional dealers and agencies',
                'plan_price': Decimal('150000.00'),  # 150,000 BIF
                'duration_days': 30,
                'category_scope': 'all',
                'max_listings': 999999,
                'max_images_per_listing': 15,
                'is_featured': True
            },
        ]

        created_count = 0
        for plan_data in plans:
            plan, created = PricingPlan.objects.get_or_create(
                pricing_name=plan_data['pricing_name'],
                defaults=plan_data
            )
            if created:
                created_count += 1
                price_str = f"{plan.plan_price:,.0f} BIF" if plan.plan_price > 0 else "FREE"
                self.stdout.write(
                    f'  ✓ Created: {plan.pricing_name} - {price_str}/month '
                    f'({plan.max_listings} listings, {plan.max_images_per_listing} images)'
                )
            else:
                self.stdout.write(f'  ⊙ Exists: {plan.pricing_name}')

        return created_count
