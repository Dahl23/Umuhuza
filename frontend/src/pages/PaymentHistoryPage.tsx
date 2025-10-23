import { useQuery } from '@tanstack/react-query';
import { format } from 'date-fns';
import { CreditCard, CheckCircle, XCircle, Clock, ArrowLeft } from 'lucide-react';
import { useNavigate } from 'react-router-dom';
import Layout from '../components/layout/Layout';
import LoadingSpinner from '../components/common/LoadingSpinner';
import Button from '../components/common/Button';
import { paymentsApi } from '../api/payments';
import type { Payment } from '../types';

export default function PaymentHistoryPage() {
  const navigate = useNavigate();

  const { data: payments, isLoading, error } = useQuery({
    queryKey: ['payments'],
    queryFn: paymentsApi.getHistory,
  });

  const getStatusIcon = (status: Payment['payment_status']) => {
    switch (status) {
      case 'successful':
        return <CheckCircle className="w-5 h-5 text-green-500" />;
      case 'failed':
        return <XCircle className="w-5 h-5 text-red-500" />;
      case 'pending':
        return <Clock className="w-5 h-5 text-yellow-500" />;
      case 'refunded':
        return <ArrowLeft className="w-5 h-5 text-blue-500" />;
      default:
        return <Clock className="w-5 h-5 text-gray-500" />;
    }
  };

  const getStatusBadge = (status: Payment['payment_status']) => {
    const styles = {
      successful: 'bg-green-100 text-green-800',
      failed: 'bg-red-100 text-red-800',
      pending: 'bg-yellow-100 text-yellow-800',
      refunded: 'bg-blue-100 text-blue-800',
    };

    return (
      <span className={`inline-flex items-center gap-1 px-3 py-1 rounded-full text-sm font-medium ${styles[status]}`}>
        {getStatusIcon(status)}
        {status.charAt(0).toUpperCase() + status.slice(1)}
      </span>
    );
  };

  const formatPaymentMethod = (method: Payment['payment_method']) => {
    const labels = {
      mobile_money: 'Mobile Money',
      card: 'Card',
      wallet: 'Wallet',
    };
    return labels[method] || method;
  };

  return (
    <Layout>
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="mb-8 flex items-center justify-between">
          <div>
            <h1 className="text-3xl font-bold text-gray-900">Payment History</h1>
            <p className="text-gray-600 mt-1">View all your payment transactions</p>
          </div>
          <Button variant="outline" onClick={() => navigate('/profile')}>
            <ArrowLeft className="w-4 h-4" />
            Back to Profile
          </Button>
        </div>

        {isLoading ? (
          <div className="flex justify-center py-20">
            <LoadingSpinner size="lg" text="Loading payments..." />
          </div>
        ) : error ? (
          <div className="text-center py-20">
            <XCircle className="w-16 h-16 text-red-500 mx-auto mb-4" />
            <p className="text-red-600 mb-4">Failed to load payment history</p>
            <Button onClick={() => window.location.reload()}>Retry</Button>
          </div>
        ) : payments && payments.length === 0 ? (
          <div className="text-center py-20">
            <CreditCard className="w-16 h-16 text-gray-400 mx-auto mb-4" />
            <h3 className="text-lg font-semibold text-gray-900 mb-2">No Payments Yet</h3>
            <p className="text-gray-600 mb-6">You haven't made any payments yet.</p>
            <Button onClick={() => navigate('/my-listings')}>
              Go to My Listings
            </Button>
          </div>
        ) : (
          <div className="bg-white rounded-lg shadow-sm border border-gray-200 overflow-hidden">
            {/* Desktop Table View */}
            <div className="hidden md:block overflow-x-auto">
              <table className="w-full">
                <thead className="bg-gray-50 border-b border-gray-200">
                  <tr>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Date
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Plan
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Amount
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Method
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Status
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Reference
                    </th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-gray-200">
                  {payments?.map((payment) => (
                    <tr key={payment.payment_id} className="hover:bg-gray-50">
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                        {format(new Date(payment.createdat), 'MMM d, yyyy')}
                        <div className="text-xs text-gray-500">
                          {format(new Date(payment.createdat), 'h:mm a')}
                        </div>
                      </td>
                      <td className="px-6 py-4 text-sm text-gray-900">
                        <div className="font-medium">{payment.pricing_id.pricing_name}</div>
                        {payment.listing_id && (
                          <div className="text-xs text-gray-500">
                            Listing #{payment.listing_id}
                          </div>
                        )}
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm font-semibold text-gray-900">
                        {parseFloat(payment.payment_amount).toLocaleString()} BIF
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-600">
                        {formatPaymentMethod(payment.payment_method)}
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap">
                        {getStatusBadge(payment.payment_status)}
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-600 font-mono">
                        {payment.payment_ref}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>

            {/* Mobile Card View */}
            <div className="md:hidden divide-y divide-gray-200">
              {payments?.map((payment) => (
                <div key={payment.payment_id} className="p-4">
                  <div className="flex items-center justify-between mb-3">
                    <span className="text-sm font-medium text-gray-900">
                      {format(new Date(payment.createdat), 'MMM d, yyyy')}
                    </span>
                    {getStatusBadge(payment.payment_status)}
                  </div>

                  <div className="space-y-2 text-sm">
                    <div className="flex justify-between">
                      <span className="text-gray-600">Plan:</span>
                      <span className="font-medium text-gray-900">{payment.pricing_id.pricing_name}</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-gray-600">Amount:</span>
                      <span className="font-semibold text-gray-900">
                        {parseFloat(payment.payment_amount).toLocaleString()} BIF
                      </span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-gray-600">Method:</span>
                      <span className="text-gray-900">{formatPaymentMethod(payment.payment_method)}</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-gray-600">Ref:</span>
                      <span className="text-gray-900 font-mono text-xs">{payment.payment_ref}</span>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Summary Stats (if payments exist) */}
        {payments && payments.length > 0 && (
          <div className="mt-8 grid grid-cols-1 md:grid-cols-3 gap-6">
            <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
              <div className="text-sm text-gray-600 mb-1">Total Payments</div>
              <div className="text-2xl font-bold text-gray-900">{payments.length}</div>
            </div>
            <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
              <div className="text-sm text-gray-600 mb-1">Successful</div>
              <div className="text-2xl font-bold text-green-600">
                {payments.filter(p => p.payment_status === 'successful').length}
              </div>
            </div>
            <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
              <div className="text-sm text-gray-600 mb-1">Total Spent</div>
              <div className="text-2xl font-bold text-primary-600">
                {payments
                  .filter(p => p.payment_status === 'successful')
                  .reduce((sum, p) => sum + parseFloat(p.payment_amount), 0)
                  .toLocaleString()} BIF
              </div>
            </div>
          </div>
        )}
      </div>
    </Layout>
  );
}
