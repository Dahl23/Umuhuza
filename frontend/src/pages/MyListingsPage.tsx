import { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { listingsApi } from '../api/listings';
import Layout from '../components/layout/Layout';
import LoadingSpinner from '../components/common/LoadingSpinner';
import Button from '../components/common/Button';
import {
  Plus, Edit, Trash2, Eye, MapPin, Calendar, TrendingUp,
  Package, CheckCircle, Clock, XCircle, Star
} from 'lucide-react';
import toast from 'react-hot-toast';
import { format } from 'date-fns';
import PaymentModal from '../components/payments/PaymentModal';

export default function MyListingsPage() {
  const navigate = useNavigate();
  const queryClient = useQueryClient();
  const [deletingId, setDeletingId] = useState<number | null>(null);
  const [paymentModalOpen, setPaymentModalOpen] = useState(false);
  const [selectedListingId, setSelectedListingId] = useState<number | null>(null);

  // Fetch user's listings
  const { data: listings, isLoading } = useQuery({
    queryKey: ['my-listings'],
    queryFn: listingsApi.getMyListings,
  });

  // Delete mutation
  const deleteMutation = useMutation({
    mutationFn: listingsApi.delete,
    onSuccess: () => {
      toast.success('Listing deleted successfully');
      queryClient.invalidateQueries({ queryKey: ['my-listings'] });
      setDeletingId(null);
    },
    onError: () => {
      toast.error('Failed to delete listing');
      setDeletingId(null);
    },
  });

  const handleDelete = (id: number, title: string) => {
    if (window.confirm(`Are you sure you want to delete "${title}"?`)) {
      setDeletingId(id);
      deleteMutation.mutate(id);
    }
  };

  const formatPrice = (price: string) => {
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'BIF',
      minimumFractionDigits: 0,
    }).format(parseFloat(price));
  };

  // Calculate stats
  const stats = listings ? {
    total: listings.length,
    active: listings.filter(l => l.listing_status === 'active').length,
    pending: listings.filter(l => l.listing_status === 'pending').length,
    sold: listings.filter(l => l.listing_status === 'sold').length,
    totalViews: listings.reduce((sum, l) => sum + l.views, 0),
  } : null;

  const getStatusColor = (status: string) => {
    const colors = {
      active: 'bg-green-100 text-green-800',
      pending: 'bg-yellow-100 text-yellow-800',
      sold: 'bg-blue-100 text-blue-800',
      expired: 'bg-gray-100 text-gray-800',
      hidden: 'bg-red-100 text-red-800',
    };
    return colors[status as keyof typeof colors] || 'bg-gray-100 text-gray-800';
  };

  const getStatusIcon = (status: string) => {
    const icons = {
      active: <CheckCircle className="w-4 h-4" />,
      pending: <Clock className="w-4 h-4" />,
      sold: <CheckCircle className="w-4 h-4" />,
      expired: <XCircle className="w-4 h-4" />,
      hidden: <XCircle className="w-4 h-4" />,
    };
    return icons[status as keyof typeof icons] || <Clock className="w-4 h-4" />;
  };

  if (isLoading) {
    return (
      <Layout>
        <div className="flex justify-center py-20">
          <LoadingSpinner size="lg" text="Loading your listings..." />
        </div>
      </Layout>
    );
  }

  return (
    <Layout>
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Header */}
        <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between mb-8">
          <div>
            <h1 className="text-3xl font-bold text-gray-900">My Listings</h1>
            <p className="text-gray-600 mt-1">Manage your listings and track performance</p>
          </div>
          <Link to="/listings/create" className="mt-4 sm:mt-0">
            <Button>
              <Plus className="w-5 h-5" />
              Create Listing
            </Button>
          </Link>
        </div>

        {/* Stats Grid */}
        {stats && (
          <div className="grid grid-cols-2 md:grid-cols-5 gap-4 mb-8">
            <div className="card">
              <div className="flex items-center gap-3">
                <div className="p-2 bg-primary-100 rounded-lg">
                  <Package className="w-6 h-6 text-primary-600" />
                </div>
                <div>
                  <p className="text-2xl font-bold text-gray-900">{stats.total}</p>
                  <p className="text-sm text-gray-600">Total</p>
                </div>
              </div>
            </div>

            <div className="card">
              <div className="flex items-center gap-3">
                <div className="p-2 bg-green-100 rounded-lg">
                  <CheckCircle className="w-6 h-6 text-green-600" />
                </div>
                <div>
                  <p className="text-2xl font-bold text-gray-900">{stats.active}</p>
                  <p className="text-sm text-gray-600">Active</p>
                </div>
              </div>
            </div>

            <div className="card">
              <div className="flex items-center gap-3">
                <div className="p-2 bg-yellow-100 rounded-lg">
                  <Clock className="w-6 h-6 text-yellow-600" />
                </div>
                <div>
                  <p className="text-2xl font-bold text-gray-900">{stats.pending}</p>
                  <p className="text-sm text-gray-600">Pending</p>
                </div>
              </div>
            </div>

            <div className="card">
              <div className="flex items-center gap-3">
                <div className="p-2 bg-blue-100 rounded-lg">
                  <CheckCircle className="w-6 h-6 text-blue-600" />
                </div>
                <div>
                  <p className="text-2xl font-bold text-gray-900">{stats.sold}</p>
                  <p className="text-sm text-gray-600">Sold</p>
                </div>
              </div>
            </div>

            <div className="card">
              <div className="flex items-center gap-3">
                <div className="p-2 bg-purple-100 rounded-lg">
                  <TrendingUp className="w-6 h-6 text-purple-600" />
                </div>
                <div>
                  <p className="text-2xl font-bold text-gray-900">{stats.totalViews}</p>
                  <p className="text-sm text-gray-600">Total Views</p>
                </div>
              </div>
            </div>
          </div>
        )}

        {/* Listings Table/Grid */}
        {!listings || listings.length === 0 ? (
          <div className="card text-center py-12">
            <Package className="w-16 h-16 mx-auto text-gray-300 mb-4" />
            <h3 className="text-xl font-semibold text-gray-900 mb-2">
              No listings yet
            </h3>
            <p className="text-gray-600 mb-6">
              Create your first listing to start selling
            </p>
            <Link to="/listings/create">
              <Button>
                <Plus className="w-5 h-5" />
                Create First Listing
              </Button>
            </Link>
          </div>
        ) : (
          <div className="space-y-4">
            {listings.map((listing) => {
              const primaryImage = listing.images.find(img => img.is_primary) || listing.images[0];
              
              return (
                <div key={listing.listing_id} className="card hover:shadow-lg transition-shadow">
                  <div className="flex flex-col sm:flex-row gap-4">
                    {/* Image */}
                    <div className="sm:w-48 h-32 sm:h-auto bg-gray-200 rounded-lg overflow-hidden flex-shrink-0">
                      {primaryImage ? (
                        <img
                          src={primaryImage.image_url}
                          alt={listing.listing_title}
                          className="w-full h-full object-cover"
                        />
                      ) : (
                        <div className="w-full h-full flex items-center justify-center">
                          <Package className="w-12 h-12 text-gray-400" />
                        </div>
                      )}
                    </div>

                    {/* Content */}
                    <div className="flex-1 min-w-0">
                      <div className="flex items-start justify-between gap-4">
                        <div className="flex-1 min-w-0">
                          <div className="flex items-center gap-2 mb-2">
                            <h3 className="text-lg font-semibold text-gray-900 truncate">
                              {listing.listing_title}
                            </h3>
                            {listing.is_featured && (
                              <span className="inline-block bg-yellow-100 text-yellow-800 text-xs px-2 py-1 rounded font-semibold">
                                FEATURED
                              </span>
                            )}
                          </div>

                          <div className="flex flex-wrap items-center gap-4 text-sm text-gray-600 mb-3">
                            <div className="flex items-center gap-1">
                              <MapPin className="w-4 h-4" />
                              <span>{listing.list_location}</span>
                            </div>
                            <div className="flex items-center gap-1">
                              <Eye className="w-4 h-4" />
                              <span>{listing.views} views</span>
                            </div>
                            <div className="flex items-center gap-1">
                              <Calendar className="w-4 h-4" />
                              <span>{format(new Date(listing.createdat), 'MMM d, yyyy')}</span>
                            </div>
                          </div>

                          <div className="flex items-center gap-3">
                            <p className="text-2xl font-bold text-primary-600">
                              {formatPrice(listing.listing_price)}
                            </p>
                            <span className={`inline-flex items-center gap-1 px-3 py-1 rounded-full text-sm font-medium ${getStatusColor(listing.listing_status)}`}>
                              {getStatusIcon(listing.listing_status)}
                              {listing.listing_status.charAt(0).toUpperCase() + listing.listing_status.slice(1)}
                            </span>
                          </div>
                        </div>

                        {/* Actions */}
                        <div className="flex sm:flex-col gap-2">
                          <Button
                            variant="outline"
                            onClick={() => navigate(`/listings/${listing.listing_id}`)}
                            title="View Listing"
                          >
                            <Eye className="w-4 h-4" />
                          </Button>
                          <Button
                            variant="outline"
                            onClick={() => navigate(`/listings/${listing.listing_id}/edit`)}
                            title="Edit Listing"
                          >
                            <Edit className="w-4 h-4" />
                          </Button>
                          {!listing.is_featured && listing.listing_status === 'active' && (
                            <Button
                              variant="outline"
                              onClick={() => {
                                setSelectedListingId(listing.listing_id);
                                setPaymentModalOpen(true);
                              }}
                              title="Promote to Featured"
                              className="border-primary-300 text-primary-700 hover:bg-primary-50"
                            >
                              <Star className="w-4 h-4" />
                            </Button>
                          )}
                          <Button
                            variant="outline"
                            onClick={() => handleDelete(listing.listing_id, listing.listing_title)}
                            disabled={deletingId === listing.listing_id}
                            title="Delete Listing"
                          >
                            <Trash2 className="w-4 h-4 text-red-600" />
                          </Button>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              );
            })}
          </div>
        )}

        {/* Payment Modal */}
        <PaymentModal
          isOpen={paymentModalOpen}
          onClose={() => {
            setPaymentModalOpen(false);
            setSelectedListingId(null);
          }}
          listingId={selectedListingId || undefined}
        />
      </div>
    </Layout>
  );
}