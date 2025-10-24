import { useQuery } from '@tanstack/react-query';
import { useNavigate } from 'react-router-dom';
import { Check, Zap, Star, Building2 } from 'lucide-react';
import Layout from '../components/layout/Layout';
import LoadingSpinner from '../components/common/LoadingSpinner';
import Button from '../components/common/Button';
import { pricingPlansApi } from '../api/payments';
import { useAuthStore } from '../store/authStore';

export default function PricingPage() {
  const navigate = useNavigate();
  const { user } = useAuthStore();

  // Fetch pricing plans
  const { data: pricingPlans, isLoading } = useQuery({
    queryKey: ['pricing-plans'],
    queryFn: () => pricingPlansApi.getAll(),
  });

  const handleSelectPlan = (planId: number) => {
    if (!user) {
      navigate('/login');
      return;
    }
    // Navigate to create listing or payment flow
    navigate(`/listings/create?plan=${planId}`);
  };

  const getPlanIcon = (planName: string) => {
    if (planName.toLowerCase().includes('free')) {
      return <Zap className="w-8 h-8 text-gray-600" />;
    }
    if (planName.toLowerCase().includes('premium')) {
      return <Star className="w-8 h-8 text-primary-600" />;
    }
    if (planName.toLowerCase().includes('dealer')) {
      return <Building2 className="w-8 h-8 text-purple-600" />;
    }
    return <Star className="w-8 h-8 text-primary-600" />;
  };

  return (
    <Layout>
      <div className="bg-gradient-to-br from-primary-50 via-white to-purple-50 py-16">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          {/* Header */}
          <div className="text-center mb-16">
            <h1 className="text-4xl font-bold text-gray-900 mb-4">
              Simple, Transparent Pricing
            </h1>
            <p className="text-xl text-gray-600 max-w-2xl mx-auto">
              Choose the perfect plan to showcase your listings and reach more buyers
            </p>
          </div>

          {/* Pricing Cards */}
          {isLoading ? (
            <div className="flex justify-center py-12">
              <LoadingSpinner size="lg" text="Loading pricing plans..." />
            </div>
          ) : (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
              {pricingPlans?.map((plan) => {
                const isFree = parseFloat(plan.plan_price) === 0;
                const isPremium = plan.pricing_name.toLowerCase().includes('premium');
                const isDealer = plan.pricing_name.toLowerCase().includes('dealer');

                return (
                  <div
                    key={plan.pricing_id}
                    className={`relative bg-white rounded-2xl shadow-lg overflow-hidden transition-all hover:shadow-2xl hover:scale-105 ${
                      isPremium ? 'border-2 border-primary-500' : 'border border-gray-200'
                    }`}
                  >
                    {/* Popular Badge */}
                    {isPremium && (
                      <div className="absolute top-0 right-0 bg-primary-500 text-white px-4 py-1 text-sm font-semibold rounded-bl-lg">
                        Most Popular
                      </div>
                    )}

                    <div className="p-8">
                      {/* Icon */}
                      <div className="mb-4">{getPlanIcon(plan.pricing_name)}</div>

                      {/* Plan Name */}
                      <h3 className="text-2xl font-bold text-gray-900 mb-2">
                        {plan.pricing_name}
                      </h3>

                      {/* Description */}
                      <p className="text-gray-600 mb-6 min-h-[48px]">
                        {plan.pricing_description}
                      </p>

                      {/* Price */}
                      <div className="mb-6">
                        {isFree ? (
                          <div>
                            <span className="text-5xl font-bold text-gray-900">Free</span>
                          </div>
                        ) : (
                          <div>
                            <span className="text-5xl font-bold text-gray-900">
                              {parseFloat(plan.plan_price).toLocaleString()}
                            </span>
                            <span className="text-gray-600 ml-2">BIF</span>
                            <div className="text-sm text-gray-500 mt-1">
                              for {plan.duration_days} days
                            </div>
                          </div>
                        )}
                      </div>

                      {/* Features */}
                      <ul className="space-y-4 mb-8">
                        <li className="flex items-start gap-3">
                          <Check className="w-5 h-5 text-green-500 flex-shrink-0 mt-0.5" />
                          <span className="text-gray-700">
                            <strong>{plan.max_listings}</strong>{' '}
                            {plan.max_listings === 1 ? 'listing' : 'active listings'}
                          </span>
                        </li>
                        <li className="flex items-start gap-3">
                          <Check className="w-5 h-5 text-green-500 flex-shrink-0 mt-0.5" />
                          <span className="text-gray-700">
                            Up to <strong>{plan.max_images_per_listing}</strong> images per
                            listing
                          </span>
                        </li>
                        <li className="flex items-start gap-3">
                          <Check className="w-5 h-5 text-green-500 flex-shrink-0 mt-0.5" />
                          <span className="text-gray-700">
                            <strong>{plan.duration_days} days</strong> listing duration
                          </span>
                        </li>
                        {plan.is_featured && (
                          <li className="flex items-start gap-3">
                            <Check className="w-5 h-5 text-green-500 flex-shrink-0 mt-0.5" />
                            <span className="text-gray-700 font-semibold text-primary-600">
                              Featured badge on listings
                            </span>
                          </li>
                        )}
                        {isDealer && (
                          <li className="flex items-start gap-3">
                            <Check className="w-5 h-5 text-green-500 flex-shrink-0 mt-0.5" />
                            <span className="text-gray-700 font-semibold text-purple-600">
                              Priority support
                            </span>
                          </li>
                        )}
                      </ul>

                      {/* CTA Button */}
                      <Button
                        fullWidth
                        variant={isPremium ? 'primary' : 'outline'}
                        onClick={() => handleSelectPlan(plan.pricing_id)}
                        className={
                          isDealer
                            ? 'bg-gradient-to-r from-purple-600 to-primary-600 hover:from-purple-700 hover:to-primary-700 text-white border-0'
                            : ''
                        }
                      >
                        {isFree ? 'Get Started Free' : 'Choose Plan'}
                      </Button>
                    </div>
                  </div>
                );
              })}
            </div>
          )}

          {/* FAQ or Additional Info */}
          <div className="mt-16 text-center">
            <p className="text-gray-600 mb-4">
              Have questions about our pricing?{' '}
              <button
                onClick={() => navigate('/contact')}
                className="text-primary-600 hover:underline font-semibold"
              >
                Contact us
              </button>
            </p>
          </div>
        </div>
      </div>
    </Layout>
  );
}
