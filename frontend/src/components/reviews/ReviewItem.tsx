import { formatDistanceToNow } from 'date-fns';
import { User as UserIcon } from 'lucide-react';
import StarRating from '../common/StarRating';
import type { Review } from '../../types';

interface ReviewItemProps {
  review: Review;
}

export default function ReviewItem({ review }: ReviewItemProps) {
  const getInitials = (firstName: string, lastName: string) => {
    return `${firstName.charAt(0)}${lastName.charAt(0)}`.toUpperCase();
  };

  return (
    <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-4">
      <div className="flex items-start gap-3">
        {/* Reviewer Avatar */}
        <div className="flex-shrink-0">
          {review.reviewer.profile_photo ? (
            <img
              src={review.reviewer.profile_photo}
              alt={review.reviewer.full_name}
              className="w-12 h-12 rounded-full object-cover"
            />
          ) : (
            <div className="w-12 h-12 rounded-full bg-primary-100 text-primary-700 flex items-center justify-center font-semibold">
              {getInitials(review.reviewer.user_firstname, review.reviewer.user_lastname)}
            </div>
          )}
        </div>

        {/* Review Content */}
        <div className="flex-1 min-w-0">
          <div className="flex items-center justify-between mb-1">
            <div>
              <h4 className="font-semibold text-gray-900">
                {review.reviewer.full_name}
              </h4>
              <div className="flex items-center gap-2 mt-1">
                <StarRating rating={review.rating} readonly size="sm" />
                <span className="text-xs text-gray-500">
                  {formatDistanceToNow(new Date(review.createdat), { addSuffix: true })}
                </span>
              </div>
            </div>
          </div>

          {review.comment && (
            <p className="text-gray-700 mt-2 text-sm leading-relaxed">
              {review.comment}
            </p>
          )}
        </div>
      </div>
    </div>
  );
}
