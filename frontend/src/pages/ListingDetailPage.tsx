import { useState } from 'react';
import { useParams, useNavigate, Link } from 'react-router-dom';
import { useQuery } from '@tanstack/react-query';
import { listingsApi } from '../api/listings';
import Layout from '../components/layout/Layout';
import LoadingSpinner from '../components/common/LoadingSpinner';
import Button from '../components/common/Button';
import ListingCard from '../components/listings/ListingCard';
import ReportModal from '../components/common/ReportModal';
import { useRequireVerification } from '../hooks/useRequireVerification';
import { 
  MapPin, Eye, Heart, Share2, Flag, MessageCircle, 
  ChevronLeft, ChevronRight, Phone, Mail, Calendar,
  ArrowLeft, ExternalLink
} from 'lucide-react';
import toast from 'react-hot-toast';
import { useAuthStore } from '../store/authStore';
import { format } from 'date-fns';

export default function ListingDetailPage() {
  
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const { isAuthenticated, user } = useAuthStore();
  const [currentImageIndex, setCurrentImageIndex] = useState(0);
  const [isFavorited, setIsFavorited] = useState(false);
  const [isReportModalOpen, setIsReportModalOpen] = useState(false);

  // Fetch listing
  const { data: listing, isLoading, error } = useQuery({
    queryKey: ['listing', id],
    queryFn: () => listingsApi.getById(Number(id)),
    enabled: !!id,
  });

  // Fetch similar listings
  const { data: similarListings } = useQuery({
    queryKey: ['similar', id],
    queryFn: () => listingsApi.getSimilar(Number(id)),
    enabled: !!id,
  });

  const handleToggleFavorite = async () => {
    if (!isAuthenticated) {
      toast.error('Please login to save favorites');
      navigate('/login');
      return;
    }

    try {
      const result = await listingsApi.toggleFavorite(Number(id));
      setIsFavorited(result.is_favorited);
      toast.success(result.is_favorited ? 'Added to favorites' : 'Removed from favorites');
    } catch (error) {
      toast.error('Failed to update favorite');
    }
  };

  const handleShare = () => {
    if (navigator.share) {
      navigator.share({
        title: listing?.listing_title,
        text: listing?.list_description,
        url: window.location.href,
      });
    } else {
      navigator.clipboard.writeText(window.location.href);
      toast.success('Link copied to clipboard!');
    }
  };
  const { checkVerification } = useRequireVerification();

  const handleContactSeller = () => {

    if (!isAuthenticated) {
      toast.error('Please login to contact seller');
      navigate('/login');
      return;
    }
    navigate(`/messages?listing=${id}`);

    if (!checkVerification('contact sellers')) {
      return;
    }
    navigate(`/messages?listing=${id}`);
  };

  const formatPrice = (price: string) => {
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'BIF',
      minimumFractionDigits: 0,
    }).format(parseFloat(price));
  };

  if (isLoading) {
    return (
      <Layout>
        <div className="flex justify-center py-20">
          <LoadingSpinner size="lg" text="Loading listing..." />
        </div>
      </Layout>
    );
  }

  if (error || !listing) {
    return (
      <Layout>
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-20 text-center">
          <p className="text-red-600 mb-4">Listing not found</p>
          <Button onClick={() => navigate('/listings')}>
            <ArrowLeft className="w-4 h-4" />
            Back to Listings
          </Button>
        </div>
      </Layout>
    );
  }

  const images = listing.images.length > 0 
  ? listing.images.sort((a, b) => a.display_order - b.display_order)
  : [{ listimage_id: 0, image_url: '/placeholder-image.jpg', is_primary: true, display_order: 0 }];

  const currentImage = images[currentImageIndex];
  const isOwner = user?.userid === listing.seller.userid;

  return (
    <Layout>
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Back Button */}
        <button
          onClick={() => navigate(-1)}
          className="flex items-center gap-2 text-gray-600 hover:text-gray-900 mb-6"
        >
          <ArrowLeft className="w-5 h-5" />
          Back
        </button>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Left Column - Images & Details */}
          <div className="lg:col-span-2">
            {/* Image Gallery */}
            <div className="mb-6">
              {/* Main Image */}
              <div className="relative h-96 bg-gray-200 rounded-lg overflow-hidden mb-4">
                <img
                  src={currentImage.image_url}
                  alt={listing.listing_title}
                  className="w-full h-full object-cover"
                />
                
                {/* Navigation Arrows */}
                {images.length > 1 && (
                  <>
                    <button
                      onClick={() => setCurrentImageIndex(Math.max(0, currentImageIndex - 1))}
                      disabled={currentImageIndex === 0}
                      className="absolute left-2 top-1/2 -translate-y-1/2 bg-white/80 hover:bg-white p-2 rounded-full disabled:opacity-50"
                    >
                      <ChevronLeft className="w-6 h-6" />
                    </button>
                    <button
                      onClick={() => setCurrentImageIndex(Math.min(images.length - 1, currentImageIndex + 1))}
                      disabled={currentImageIndex === images.length - 1}
                      className="absolute right-2 top-1/2 -translate-y-1/2 bg-white/80 hover:bg-white p-2 rounded-full disabled:opacity-50"
                    >
                      <ChevronRight className="w-6 h-6" />
                    </button>
                  </>
                )}

                {/* Image Counter */}
                <div className="absolute bottom-4 right-4 bg-black/70 text-white px-3 py-1 rounded-full text-sm">
                  {currentImageIndex + 1} / {images.length}
                </div>

                {/* Featured Badge */}
                {listing.is_featured && (
                  <div className="absolute top-4 left-4 bg-yellow-500 text-white font-bold px-3 py-1 rounded">
                    FEATURED
                  </div>
                )}
              </div>

              {/* Thumbnails */}
              
              {images.length > 1 && (
                <div className="grid grid-cols-5 gap-2">
                  {images.map((img, index) => (
                    <button
                      key={img.listimage_id ?? index}
                      onClick={() => setCurrentImageIndex(index)}
                      className={`h-20 rounded-lg overflow-hidden border-2 transition-colors ${
                        index === currentImageIndex
                          ? 'border-primary-600'
                          : 'border-gray-200 hover:border-gray-400'
                      }`}
                    >
                      <img
                        src={img.image_url}
                        alt=""
                        className="w-full h-full object-cover"
                      />
                    </button>
                  ))}
                </div>
              )}
            </div>

            {/* Listing Details */}
            <div className="card">
              <div className="flex items-start justify-between mb-4">
                <div className="flex-1">
                  <h1 className="text-3xl font-bold text-gray-900 mb-2">
                    {listing.listing_title}
                  </h1>
                  <div className="flex items-center gap-4 text-gray-600">
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
                </div>
              </div>

              {/* Price */}
              <div className="text-4xl font-bold text-primary-600 mb-6">
                {formatPrice(listing.listing_price)}
              </div>

              {/* Category */}
              <div className="mb-6">
                <span className="inline-block bg-primary-100 text-primary-800 px-3 py-1 rounded-full text-sm font-medium">
                  {listing.category.cat_name}
                </span>
              </div>

              {/* Description */}
              <div className="prose max-w-none">
                <h2 className="text-xl font-semibold mb-3">Description</h2>
                <p className="text-gray-700 whitespace-pre-line">
                  {listing.list_description}
                </p>
              </div>
            </div>
          </div>

          {/* Right Column - Seller Info & Actions */}
          <div className="lg:col-span-1">
            <div className="sticky top-24 space-y-4">
              {/* Actions Card */}
              <div className="card">
                <div className="flex gap-2 mb-4">
                  <Button
                    onClick={handleToggleFavorite}
                    variant="outline"
                    className="flex-1"
                  >
                    <Heart className={`w-5 h-5 ${isFavorited ? 'fill-current text-red-500' : ''}`} />
                  </Button>
                  <Button onClick={handleShare} variant="outline" className="flex-1">
                    <Share2 className="w-5 h-5" />
                  </Button>
                  <Button 
                    onClick={() => window.open(`https://www.google.com/maps/search/?api=1&query=${encodeURIComponent(listing.list_location)}`, '_blank')}
                    variant="outline" 
                    className="flex-1"
                    title="View on Map"
                  >
                    <ExternalLink className="w-5 h-5" />
                  </Button>
                  <Button
                    variant="outline"
                    className="flex-1"
                    title="Report Listing"
                    onClick={() => setIsReportModalOpen(true)}
                  >
                    <Flag className="w-5 h-5" />
                  </Button>
                </div>

                {!isOwner && (
                  <Button onClick={handleContactSeller} fullWidth>
                    <MessageCircle className="w-5 h-5" />
                    Contact Seller
                  </Button>
                )}

                {isOwner && (
                  <div className="space-y-2">
                    <Button 
                      onClick={() => navigate(`/listings/${id}/edit`)}
                      fullWidth
                    >
                      Edit Listing
                    </Button>
                    <p className="text-sm text-gray-500 text-center">
                      This is your listing
                    </p>
                  </div>
                )}
              </div>

              {/* Seller Info Card */}
              <div className="card">
                <h3 className="font-semibold mb-4">Seller Information</h3>
                
                <Link 
                  to={`/users/${listing.seller.userid}`}
                  className="flex items-center gap-3 mb-4 hover:bg-gray-50 p-2 rounded-lg transition-colors"
                >
                  <div className="w-12 h-12 bg-primary-100 rounded-full flex items-center justify-center text-primary-600 font-semibold text-lg">
                    {listing.seller?.user_firstname?.[0] || listing.seller?.full_name?.[0] || '?'}
                  </div>
                  <div className="flex-1">
                    <p className="font-semibold text-gray-900">
                      {listing.seller?.full_name || 'Unknown'}
                    </p>
                    {listing.seller?.is_verified && (
                      <p className="text-sm text-green-600 flex items-center gap-1">
                        ✓ Verified User
                      </p>
                    )}
                    <p className="text-sm text-gray-500">
                      {listing.seller?.user_role || 'user'}
                    </p>
                  </div>
                </Link>

                <div className="space-y-2 pt-4 border-t border-gray-200">
                  
                  <a href={`tel:${listing.seller?.phone_number}`}
                    className="flex items-center gap-2 text-gray-700 hover:text-primary-600"
                  >
                    <Phone className="w-4 h-4" />
                    <span className="text-sm">{listing.seller?.phone_number || 'N/A'}</span>
                  </a>
                  
                  <a href={`mailto:${listing.seller?.email}`}
                    className="flex items-center gap-2 text-gray-700 hover:text-primary-600"
                  >
                    <Mail className="w-4 h-4" />
                    <span className="text-sm">{listing.seller?.email || 'N/A'}</span>
                  </a>
                </div>
              </div>

              {/* Safety Tips Card */}
              <div className="card bg-yellow-50 border border-yellow-200">
                <h3 className="font-semibold mb-2 text-yellow-900">Safety Tips</h3>
                <ul className="text-sm text-yellow-800 space-y-1">
                  <li>• Meet in a public place</li>
                  <li>• Check the item before payment</li>
                  <li>• Don't pay in advance</li>
                  <li>• Report suspicious listings</li>
                </ul>
              </div>
            </div>
          </div>
        </div>

        {/* Similar Listings */}
        {similarListings && similarListings.length > 0 && (
          <div className="mt-16">
            <h2 className="text-2xl font-bold mb-6">Similar Listings</h2>
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
              {similarListings.slice(0, 4).map((listing) => (
                <ListingCard key={listing.listing_id} listing={listing} />
              ))}
            </div>
          </div>
        )}

        {/* Report Modal */}
        <ReportModal
          isOpen={isReportModalOpen}
          onClose={() => setIsReportModalOpen(false)}
          listingId={Number(id)}
          reportType="listing"
          itemTitle={listing?.listing_title}
        />
      </div>
    </Layout>
  );
}