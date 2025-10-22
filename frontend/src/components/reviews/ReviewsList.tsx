import { useQuery } from '@tanstack/react-query';
import { Star } from 'lucide-react';
import StarRating from '../common/StarRating';
import ReviewItem from './ReviewItem';
import { reviewsApi } from '../../api/reviews';

interface ReviewsListProps {
  userId: number;
  showTitle?: boolean;
}

export default function ReviewsList({ userId, showTitle = true }: ReviewsListProps) {
  const { data, isLoading, error } = useQuery({
    queryKey: ['reviews', userId],
    queryFn: () => reviewsApi.getUserReviews(userId),
  });

  if (isLoading) {
    return (
      <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
        <div className="animate-pulse">
          <div className="h-6 bg-gray-200 rounded w-32 mb-4"></div>
          <div className="space-y-4">
            <div className="h-24 bg-gray-200 rounded"></div>
            <div className="h-24 bg-gray-200 rounded"></div>
            <div className="h-24 bg-gray-200 rounded"></div>
          </div>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
        <p className="text-red-600">Failed to load reviews</p>
      </div>
    );
  }

  if (!data) {
    return null;
  }

  const { average_rating, total_reviews, reviews } = data;

  return (
    <div className="space-y-4">
      {showTitle && (
        <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
          <div className="flex items-center justify-between mb-4">
            <h3 className="text-xl font-bold text-gray-900">Reviews</h3>
            {total_reviews > 0 && (
              <div className="flex items-center gap-2">
                <StarRating
                  rating={Math.round(average_rating)}
                  readonly
                  size="md"
                />
                <span className="text-lg font-semibold text-gray-900">
                  {average_rating.toFixed(1)}
                </span>
                <span className="text-sm text-gray-600">
                  ({total_reviews} {total_reviews === 1 ? 'review' : 'reviews'})
                </span>
              </div>
            )}
          </div>

          {total_reviews === 0 && (
            <div className="text-center py-8">
              <Star className="w-12 h-12 text-gray-300 mx-auto mb-3" />
              <p className="text-gray-500">No reviews yet</p>
              <p className="text-sm text-gray-400 mt-1">
                Be the first to review this seller
              </p>
            </div>
          )}
        </div>
      )}

      {reviews.length > 0 && (
        <div className="space-y-3">
          {reviews.map((review) => (
            <ReviewItem key={review.ratingrev_id} review={review} />
          ))}
        </div>
      )}
    </div>
  );
}
