import { useNavigate } from 'react-router-dom';
import { useAuthStore } from '../store/authStore';
import Layout from '../components/layout/Layout';
import Button from '../components/common/Button';
import ReviewsList from '../components/reviews/ReviewsList';
import {
  Mail, Phone, Calendar, Shield, Edit, LogOut,
  CheckCircle, XCircle,
  Heart
} from 'lucide-react';
import { format } from 'date-fns';
import toast from 'react-hot-toast';

export default function ProfilePage() {
  const navigate = useNavigate();
  const { user, logout } = useAuthStore();

  if (!user) {
    navigate('/login');
    return null;
  }

  const handleLogout = () => {
    logout();
    toast.success('Logged out successfully');
    navigate('/');
  };

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
              <div className="w-20 h-20 bg-primary-100 rounded-full flex items-center justify-center text-primary-600 font-bold text-3xl">
                {user.user_firstname[0]}{user.user_lastname[0]}
              </div>
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