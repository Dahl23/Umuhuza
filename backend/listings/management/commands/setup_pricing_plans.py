from django.core.management.base import BaseCommand
from listings.models import PricingPlan


class Command(BaseCommand):
    help = 'Setup pricing plans based on approved specifications'

    def handle(self, *args, **options):
        plans = [
            {
                'pricing_name': 'Basic Plan',
                'pricing_description': 'Perfect for occasional sellers',
                'plan_price': 0,
                'duration_days': 60,
                'category_scope': 'all',
                'max_listings': 1,
                'max_images_per_listing': 5,
                'is_featured': False,
                'is_active': True,
            },
            {
                'pricing_name': 'Premium Plan',
                'pricing_description': 'Boost your listings with featured placement',
                'plan_price': 20000,
                'duration_days': 90,
                'category_scope': 'all',
                'max_listings': 10,
                'max_images_per_listing': 10,
                'is_featured': True,
                'is_active': True,
            },
            {
                'pricing_name': 'Dealer Monthly',
                'pricing_description': 'Unlimited listings for professional dealers',
                'plan_price': 50000,
                'duration_days': 30,
                'category_scope': 'all',
                'max_listings': 999999,  # Effectively unlimited
                'max_images_per_listing': 15,
                'is_featured': True,
                'is_active': True,
            },
        ]

        for plan_data in plans:
            plan, created = PricingPlan.objects.update_or_create(
                pricing_name=plan_data['pricing_name'],
                defaults=plan_data
            )

            if created:
                self.stdout.write(self.style.SUCCESS(f'✓ Created: {plan.pricing_name}'))
            else:
                self.stdout.write(self.style.WARNING(f'⟳ Updated: {plan.pricing_name}'))

        self.stdout.write(self.style.SUCCESS('\n✅ Pricing plans setup complete!'))
        self.stdout.write(self.style.SUCCESS(f'Total plans: {PricingPlan.objects.filter(is_active=True).count()}'))
