import { useState } from 'react';
import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query';
import { useNavigate } from 'react-router-dom';
import { toast } from 'react-hot-toast';
import { X, CreditCard, Smartphone, Check } from 'lucide-react';
import { paymentsApi, pricingPlansApi } from '../../api/payments';
import LoadingSpinner from '../common/LoadingSpinner';
import type { PaymentInitiateData } from '../../types';

interface PaymentModalProps {
  isOpen: boolean;
  onClose: () => void;
  listingId?: number;
  categoryScope?: 'all' | 'real_estate' | 'vehicle';
}

export default function PaymentModal({
  isOpen,
  onClose,
  listingId,
  categoryScope = 'all',
}: PaymentModalProps) {
  const [selectedPlan, setSelectedPlan] = useState<number | null>(null);
  const [paymentMethod, setPaymentMethod] = useState<'mobile_money' | 'card'>('mobile_money');
  const [phoneNumber, setPhoneNumber] = useState('');
  const navigate = useNavigate();
  const queryClient = useQueryClient();

  // Fetch pricing plans
  const { data: pricingPlans, isLoading } = useQuery({
    queryKey: ['pricing-plans', categoryScope],
    queryFn: () => pricingPlansApi.getAll(),
    enabled: isOpen,
  });

  // Initiate payment mutation
  const initiateMutation = useMutation({
    mutationFn: async (data: PaymentInitiateData) => {
      return paymentsApi.initiate(data);
    },
    onSuccess: (data) => {
      toast.success(data.message);
      // Navigate to payment verification page
      navigate(`/payment/verify?ref=${data.payment_ref}`);
      onClose();
    },
    onError: (error: any) => {
      const message = error.response?.data?.error || 'Payment initiation failed';
      toast.error(message);
    },
  });

  const handlePayment = () => {
    if (!selectedPlan) {
      toast.error('Please select a pricing plan');
      return;
    }

    if (paymentMethod === 'mobile_money' && !phoneNumber) {
      toast.error('Please enter your phone number');
      return;
    }

    initiateMutation.mutate({
      pricing_id: selectedPlan,
      listing_id: listingId,
      payment_method: paymentMethod,
      phone_number: paymentMethod === 'mobile_money' ? phoneNumber : undefined,
    });
  };

  if (!isOpen) return null;

  const selectedPlanData = pricingPlans?.find(p => p.pricing_id === selectedPlan);

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
      <div className="bg-white rounded-lg max-w-4xl w-full max-h-[90vh] overflow-y-auto">
        {/* Header */}
        <div className="sticky top-0 bg-white border-b border-gray-200 p-6 flex items-center justify-between">
          <h2 className="text-2xl font-bold text-gray-900">Select a Plan</h2>
          <button
            onClick={onClose}
            className="text-gray-400 hover:text-gray-600 transition-colors"
          >
            <X className="w-6 h-6" />
          </button>
        </div>

        {/* Content */}
        <div className="p-6">
          {isLoading ? (
            <div className="flex justify-center py-12">
              <LoadingSpinner size="lg" text="Loading plans..." />
            </div>
          ) : (
            <>
              {/* Pricing Plans Grid */}
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 mb-8">
                {pricingPlans?.filter(plan => plan.is_featured).map((plan) => (
                  <div
                    key={plan.pricing_id}
                    onClick={() => setSelectedPlan(plan.pricing_id)}
                    className={`relative border-2 rounded-lg p-6 cursor-pointer transition-all ${
                      selectedPlan === plan.pricing_id
                        ? 'border-primary-600 bg-primary-50'
                        : 'border-gray-200 hover:border-primary-300'
                    }`}
                  >
                    {/* Selected Checkmark */}
                    {selectedPlan === plan.pricing_id && (
                      <div className="absolute top-4 right-4 w-6 h-6 bg-primary-600 rounded-full flex items-center justify-center">
                        <Check className="w-4 h-4 text-white" />
                      </div>
                    )}

                    {/* Plan Name */}
                    <h3 className="text-xl font-bold text-gray-900 mb-2">
                      {plan.pricing_name}
                    </h3>

                    {/* Price */}
                    <div className="mb-4">
                      <span className="text-3xl font-bold text-primary-600">
                        {parseFloat(plan.plan_price).toLocaleString()} BIF
                      </span>
                      <span className="text-gray-600 ml-2">
                        /{plan.duration_days} days
                      </span>
                    </div>

                    {/* Description */}
                    <p className="text-gray-600 text-sm mb-4">
                      {plan.pricing_description}
                    </p>

                    {/* Features */}
                    <ul className="space-y-2 text-sm">
                      <li className="flex items-center gap-2 text-gray-700">
                        <Check className="w-4 h-4 text-green-500" />
                        Up to {plan.max_listings} listing{plan.max_listings > 1 ? 's' : ''}
                      </li>
                      <li className="flex items-center gap-2 text-gray-700">
                        <Check className="w-4 h-4 text-green-500" />
                        {plan.max_images_per_listing} images per listing
                      </li>
                      {plan.is_featured && (
                        <li className="flex items-center gap-2 text-gray-700">
                          <Check className="w-4 h-4 text-green-500" />
                          <span className="font-semibold text-primary-600">Featured badge</span>
                        </li>
                      )}
                      <li className="flex items-center gap-2 text-gray-700">
                        <Check className="w-4 h-4 text-green-500" />
                        {plan.duration_days} days active
                      </li>
                    </ul>
                  </div>
                ))}
              </div>

              {/* Payment Method Selection */}
              {selectedPlan && (
                <div className="bg-gray-50 rounded-lg p-6 mb-6">
                  <h3 className="text-lg font-semibold text-gray-900 mb-4">
                    Payment Method
                  </h3>

                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-6">
                    {/* Mobile Money */}
                    <button
                      onClick={() => setPaymentMethod('mobile_money')}
                      className={`flex items-center gap-3 p-4 border-2 rounded-lg transition-all ${
                        paymentMethod === 'mobile_money'
                          ? 'border-primary-600 bg-primary-50'
                          : 'border-gray-200 hover:border-primary-300'
                      }`}
                    >
                      <Smartphone className="w-6 h-6 text-primary-600" />
                      <div className="text-left">
                        <div className="font-semibold text-gray-900">Mobile Money</div>
                        <div className="text-sm text-gray-600">Lumicash, EcoCash</div>
                      </div>
                      {paymentMethod === 'mobile_money' && (
                        <Check className="w-5 h-5 text-primary-600 ml-auto" />
                      )}
                    </button>

                    {/* Card (disabled for now) */}
                    <button
                      disabled
                      className="flex items-center gap-3 p-4 border-2 rounded-lg opacity-50 cursor-not-allowed border-gray-200"
                    >
                      <CreditCard className="w-6 h-6 text-gray-400" />
                      <div className="text-left">
                        <div className="font-semibold text-gray-900">Card Payment</div>
                        <div className="text-sm text-gray-600">Coming soon</div>
                      </div>
                    </button>
                  </div>

                  {/* Phone Number Input (for Mobile Money) */}
                  {paymentMethod === 'mobile_money' && (
                    <div>
                      <label htmlFor="phone" className="block text-sm font-medium text-gray-700 mb-2">
                        Phone Number
                      </label>
                      <input
                        type="tel"
                        id="phone"
                        value={phoneNumber}
                        onChange={(e) => setPhoneNumber(e.target.value)}
                        placeholder="+257 79 123 456"
                        className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
                      />
                      <p className="text-xs text-gray-500 mt-1">
                        You'll receive a payment prompt on this number
                      </p>
                    </div>
                  )}
                </div>
              )}

              {/* Summary & Confirm Button */}
              {selectedPlanData && (
                <div className="bg-primary-50 border border-primary-200 rounded-lg p-6">
                  <div className="flex items-center justify-between mb-4">
                    <span className="text-gray-700 font-medium">Selected Plan:</span>
                    <span className="text-gray-900 font-bold">{selectedPlanData.pricing_name}</span>
                  </div>
                  <div className="flex items-center justify-between mb-6">
                    <span className="text-gray-700 font-medium">Total Amount:</span>
                    <span className="text-2xl font-bold text-primary-600">
                      {parseFloat(selectedPlanData.plan_price).toLocaleString()} BIF
                    </span>
                  </div>

                  <button
                    onClick={handlePayment}
                    disabled={initiateMutation.isPending}
                    className="btn btn-primary w-full disabled:opacity-50 disabled:cursor-not-allowed"
                  >
                    {initiateMutation.isPending ? 'Processing...' : 'Proceed to Payment'}
                  </button>
                </div>
              )}
            </>
          )}
        </div>
      </div>
    </div>
  );
}
