import { useNavigate } from 'react-router-dom';
import { useAuthStore } from '../store/authStore';
import { useQuery } from '@tanstack/react-query';
import { listingsApi } from '../api/listings';
import Layout from '../components/layout/Layout';
import Button from '../components/common/Button';
import ReviewsList from '../components/reviews/ReviewsList';
import {
  Mail, Phone, Calendar, Shield, Edit, LogOut,
  CheckCircle, XCircle,
  Heart, Building2,
  Star,
  Zap
} from 'lucide-react';
import { format } from 'date-fns';
import toast from 'react-hot-toast';
import Avatar from '../components/common/Avatar';

export default function ProfilePage() {
  const navigate = useNavigate();
  const { user, logout } = useAuthStore();

  // Fetch user's subscription
  const { data: subscriptionData } = useQuery({
    queryKey: ['current-subscription'],
    queryFn: listingsApi.getCurrentSubscription,
    enabled: !!user,
  });

  if (!user) {
    navigate('/login');
    return null;
  }

  const handleLogout = () => {
    logout();
    toast.success('Logged out successfully');
    navigate('/');
  };

  const subscription = subscriptionData?.subscription;

  return (
    <Layout>
      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900">My Profile</h1>
          <p className="text-gray-600 mt-1">Manage your account information</p>
        </div>

        {/* Profile Card */}
        <div className="card mb-6">
          <div className="flex items-start justify-between mb-6">
            <div className="flex items-center gap-4">
              <Avatar
                src={user.profile_photo}
                firstName={user.user_firstname}
                lastName={user.user_lastname}
                size="xl"
              />
              <div>
                <h2 className="text-2xl font-bold text-gray-900">{user.full_name}</h2>
                <p className="text-gray-600 capitalize">{user.user_role}</p>
                <div className="flex items-center gap-2 mt-2">
                  {user.is_verified ? (
                    <span className="inline-flex items-center gap-1 text-sm text-green-600">
                      <CheckCircle className="w-4 h-4" />
                      Verified Account
                    </span>
                  ) : (
                    <span className="inline-flex items-center gap-1 text-sm text-yellow-600">
                      <XCircle className="w-4 h-4" />
                      Not Verified
                    </span>
                  )}
                </div>
              </div>
            </div>
            <Button variant="outline" onClick={() => navigate('/profile/edit')}>
              <Edit className="w-4 h-4" />
              Edit Profile
            </Button>
          </div>

          {/* Info Grid */}
          <div className="space-y-4 border-t border-gray-200 pt-6">
            <div className="flex items-center gap-3">
              <Mail className="w-5 h-5 text-gray-400" />
              <div className="flex-1">
                <p className="text-sm text-gray-600">Email</p>
                <p className="font-medium text-gray-900">{user.email}</p>
              </div>
              {user.email_verified ? (
                <CheckCircle className="w-5 h-5 text-green-500" />
              ) : (
                <XCircle className="w-5 h-5 text-red-500" />
              )}
            </div>

            <div className="flex items-center gap-3">
              <Phone className="w-5 h-5 text-gray-400" />
              <div className="flex-1">
                <p className="text-sm text-gray-600">Phone</p>
                <p className="font-medium text-gray-900">{user.phone_number}</p>
              </div>
              {user.phone_verified ? (
                <CheckCircle className="w-5 h-5 text-green-500" />
              ) : (
                <XCircle className="w-5 h-5 text-red-500" />
              )}
            </div>

            <div className="flex items-center gap-3">
              <Calendar className="w-5 h-5 text-gray-400" />
              <div>
                <p className="text-sm text-gray-600">Member Since</p>
                <p className="font-medium text-gray-900">
                  {format(new Date(user.date_joined), 'MMMM d, yyyy')}
                </p>
              </div>
            </div>
          </div>
        </div>

        {/* Current Subscription */}
        {subscription && (
          <div className="card mb-6">
            <h3 className="font-semibold mb-4 flex items-center gap-2">
              <Star className="w-5 h-5 text-primary-600" />
              Current Plan
            </h3>
            <div className="bg-gradient-to-br from-primary-50 to-purple-50 rounded-lg p-6">
              <div className="flex items-start justify-between mb-4">
                <div>
                  <h4 className="text-xl font-bold text-gray-900 mb-1">
                    {subscription.plan.pricing_name}
                  </h4>
                  <p className="text-sm text-gray-600">
                    {subscription.plan.pricing_description}
                  </p>
                </div>
                {parseFloat(subscription.plan.plan_price) === 0 ? (
                  <Zap className="w-8 h-8 text-gray-600" />
                ) : (
                  <Star className="w-8 h-8 text-primary-600" />
                )}
              </div>

              <div className="grid grid-cols-2 gap-4 mb-4">
                <div className="bg-white rounded-lg p-3">
                  <p className="text-xs text-gray-600 mb-1">Listings Used</p>
                  <p className="text-2xl font-bold text-gray-900">
                    {subscription.listings_used} / {subscription.plan.max_listings}
                  </p>
                </div>
                <div className="bg-white rounded-lg p-3">
                  <p className="text-xs text-gray-600 mb-1">Remaining</p>
                  <p className="text-2xl font-bold text-primary-600">
                    {subscription.remaining_listings}
                  </p>
                </div>
              </div>

              {subscription.expires_at && (
                <p className="text-sm text-gray-600 mb-4">
                  Expires: {format(new Date(subscription.expires_at), 'MMMM d, yyyy')}
                </p>
              )}

              {subscription.remaining_listings === 0 && (
                <Button
                  fullWidth
                  onClick={() => navigate('/pricing')}
                  className="bg-gradient-to-r from-primary-600 to-purple-600 hover:from-primary-700 hover:to-purple-700"
                >
                  Upgrade Plan
                </Button>
              )}
            </div>
          </div>
        )}

        {/* Badges */}
        {user.badges && user.badges.length > 0 && (
          <div className="card mb-6">
            <h3 className="font-semibold mb-4 flex items-center gap-2">
              <Shield className="w-5 h-5 text-primary-600" />
              My Badges
            </h3>
            <div className="flex flex-wrap gap-2">
              {user.badges.map((badge) => (
                <span
                  key={badge.userbadge_id}
                  className="inline-flex items-center gap-1 bg-primary-100 text-primary-800 px-3 py-1 rounded-full text-sm font-medium"
                >
                  <Shield className="w-4 h-4" />
                  {badge.badge_type.replace('_', ' ').toUpperCase()}
                </span>
              ))}
            </div>
          </div>
        )}

        {/* My Reviews */}
        <div className="mb-6">
          <ReviewsList userId={user.userid} />
        </div>

        {/* Verification Status */}
        {!user.is_verified && (
          <div className="card bg-yellow-50 border border-yellow-200 mb-6">
            <h3 className="font-semibold text-yellow-900 mb-2">
              Complete Your Verification
            </h3>
            <p className="text-sm text-yellow-800 mb-4">
              Verify your account to access all features and build trust with other users.
            </p>
            <Button onClick={() => navigate('/verify')}>
              Verify Now
            </Button>
          </div>
        )}

        {/* Actions */}
        <div className="space-y-3">
          <Button
            variant="outline"
            fullWidth
            onClick={() => navigate('/my-listings')}
          >
            My Listings
          </Button>
          <Button
            variant="outline"
            fullWidth
            onClick={() => navigate('/favorites')}
          >
            <Heart className="w-4 h-4" />
            My Favorites
          </Button>
          <Button
            variant="outline"
            fullWidth
            onClick={() => navigate('/payments/history')}
          >
            Payment History
          </Button>
          {user.user_role !== 'dealer' && (
            <Button
              fullWidth
              onClick={() => navigate('/become-dealer')}
              className="bg-gradient-to-r from-primary-600 to-purple-600 hover:from-primary-700 hover:to-purple-700"
            >
              <Building2 className="w-4 h-4" />
              Become a Dealer
            </Button>
          )}
          <Button
            variant="danger"
            fullWidth
            onClick={handleLogout}
          >
            <LogOut className="w-4 h-4" />
            Logout
          </Button>
        </div>
      </div>
    </Layout>
  );
}