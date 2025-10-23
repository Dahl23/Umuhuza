import { useEffect, useState } from 'react';
import { useSearchParams, useNavigate } from 'react-router-dom';
import { useMutation } from '@tanstack/react-query';
import { toast } from 'react-hot-toast';
import { CheckCircle, XCircle, Loader2, ArrowLeft } from 'lucide-react';
import Layout from '../components/layout/Layout';
import Button from '../components/common/Button';
import { paymentsApi } from '../api/payments';

export default function PaymentVerifyPage() {
  const [searchParams] = useSearchParams();
  const navigate = useNavigate();
  const paymentRef = searchParams.get('ref');
  const [verificationStatus, setVerificationStatus] = useState<'pending' | 'success' | 'failed'>('pending');

  const verifyMutation = useMutation({
    mutationFn: async () => {
      if (!paymentRef) throw new Error('Payment reference not found');
      return paymentsApi.verify({ payment_ref: paymentRef });
    },
    onSuccess: (data) => {
      setVerificationStatus('success');
      toast.success('Payment verified successfully!');
    },
    onError: (error: any) => {
      setVerificationStatus('failed');
      const message = error.response?.data?.error || 'Payment verification failed';
      toast.error(message);
    },
  });

  // Auto-verify after 3 seconds (simulating payment processing)
  useEffect(() => {
    if (!paymentRef) {
      setVerificationStatus('failed');
      return;
    }

    const timer = setTimeout(() => {
      verifyMutation.mutate();
    }, 3000);

    return () => clearTimeout(timer);
  }, [paymentRef]);

  if (!paymentRef) {
    return (
      <Layout>
        <div className="max-w-2xl mx-auto px-4 sm:px-6 lg:px-8 py-20 text-center">
          <XCircle className="w-20 h-20 text-red-500 mx-auto mb-6" />
          <h1 className="text-3xl font-bold text-gray-900 mb-4">Invalid Payment Link</h1>
          <p className="text-gray-600 mb-8">
            The payment reference is missing or invalid.
          </p>
          <Button onClick={() => navigate('/')}>
            <ArrowLeft className="w-4 h-4" />
            Back to Home
          </Button>
        </div>
      </Layout>
    );
  }

  return (
    <Layout>
      <div className="max-w-2xl mx-auto px-4 sm:px-6 lg:px-8 py-20">
        {/* Pending State */}
        {verificationStatus === 'pending' && (
          <div className="text-center">
            <div className="mb-8">
              <Loader2 className="w-20 h-20 text-primary-600 mx-auto animate-spin" />
            </div>
            <h1 className="text-3xl font-bold text-gray-900 mb-4">
              Processing Your Payment
            </h1>
            <p className="text-gray-600 mb-4">
              Please wait while we verify your payment...
            </p>
            <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-4 mt-6">
              <p className="text-sm text-yellow-800">
                <strong>Payment Reference:</strong> {paymentRef}
              </p>
            </div>
            <p className="text-xs text-gray-500 mt-4">
              This usually takes a few seconds. Please don't close this page.
            </p>
          </div>
        )}

        {/* Success State */}
        {verificationStatus === 'success' && (
          <div className="text-center">
            <div className="mb-8">
              <CheckCircle className="w-20 h-20 text-green-500 mx-auto" />
            </div>
            <h1 className="text-3xl font-bold text-gray-900 mb-4">
              Payment Successful!
            </h1>
            <p className="text-gray-600 mb-8">
              Your payment has been processed successfully. Your listing is now featured and will receive more visibility!
            </p>

            <div className="bg-green-50 border border-green-200 rounded-lg p-6 mb-8">
              <h2 className="font-semibold text-green-900 mb-3">What's Next?</h2>
              <ul className="text-left text-green-800 space-y-2 text-sm">
                <li className="flex items-start gap-2">
                  <CheckCircle className="w-4 h-4 text-green-600 flex-shrink-0 mt-0.5" />
                  <span>Your listing is now marked as "Featured"</span>
                </li>
                <li className="flex items-start gap-2">
                  <CheckCircle className="w-4 h-4 text-green-600 flex-shrink-0 mt-0.5" />
                  <span>It will appear at the top of search results</span>
                </li>
                <li className="flex items-start gap-2">
                  <CheckCircle className="w-4 h-4 text-green-600 flex-shrink-0 mt-0.5" />
                  <span>Your listing will get more views and inquiries</span>
                </li>
                <li className="flex items-start gap-2">
                  <CheckCircle className="w-4 h-4 text-green-600 flex-shrink-0 mt-0.5" />
                  <span>You can track payment history in your profile</span>
                </li>
              </ul>
            </div>

            <div className="space-y-3">
              <Button onClick={() => navigate('/my-listings')} fullWidth>
                View My Listings
              </Button>
              <Button variant="outline" onClick={() => navigate('/payments/history')} fullWidth>
                View Payment History
              </Button>
            </div>
          </div>
        )}

        {/* Failed State */}
        {verificationStatus === 'failed' && (
          <div className="text-center">
            <div className="mb-8">
              <XCircle className="w-20 h-20 text-red-500 mx-auto" />
            </div>
            <h1 className="text-3xl font-bold text-gray-900 mb-4">
              Payment Failed
            </h1>
            <p className="text-gray-600 mb-8">
              We couldn't verify your payment. This could be due to:
            </p>

            <div className="bg-red-50 border border-red-200 rounded-lg p-6 mb-8 text-left">
              <ul className="text-red-800 space-y-2 text-sm">
                <li className="flex items-start gap-2">
                  <span className="text-red-600">•</span>
                  <span>Insufficient funds in your mobile money account</span>
                </li>
                <li className="flex items-start gap-2">
                  <span className="text-red-600">•</span>
                  <span>Payment was cancelled</span>
                </li>
                <li className="flex items-start gap-2">
                  <span className="text-red-600">•</span>
                  <span>Network or connection issues</span>
                </li>
                <li className="flex items-start gap-2">
                  <span className="text-red-600">•</span>
                  <span>Invalid payment details</span>
                </li>
              </ul>
            </div>

            <div className="space-y-3">
              <Button
                onClick={() => {
                  setVerificationStatus('pending');
                  verifyMutation.mutate();
                }}
                fullWidth
                disabled={verifyMutation.isPending}
              >
                {verifyMutation.isPending ? 'Retrying...' : 'Retry Payment Verification'}
              </Button>
              <Button variant="outline" onClick={() => navigate('/my-listings')} fullWidth>
                Back to My Listings
              </Button>
            </div>

            <p className="text-sm text-gray-500 mt-6">
              If you continue to experience issues, please contact support with reference: <strong>{paymentRef}</strong>
            </p>
          </div>
        )}
      </div>
    </Layout>
  );
}
