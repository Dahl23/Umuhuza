import { useState } from 'react';
import { useMutation, useQueryClient } from '@tanstack/react-query';
import { toast } from 'react-hot-toast';
import StarRating from '../common/StarRating';
import { reviewsApi } from '../../api/reviews';
import type { ReviewCreateData } from '../../types';

interface ReviewFormProps {
  reviewedUserId: number;
  listingId?: number;
  onSuccess?: () => void;
}

export default function ReviewForm({
  reviewedUserId,
  listingId,
  onSuccess,
}: ReviewFormProps) {
  const [rating, setRating] = useState(0);
  const [comment, setComment] = useState('');
  const queryClient = useQueryClient();

  const createMutation = useMutation({
    mutationFn: async (data: ReviewCreateData) => {
      return reviewsApi.create(data);
    },
    onSuccess: () => {
      toast.success('Review submitted successfully!');
      setRating(0);
      setComment('');
      queryClient.invalidateQueries({ queryKey: ['reviews', reviewedUserId] });
      onSuccess?.();
    },
    onError: (error: any) => {
      const message = error.response?.data?.error || 'Failed to submit review';
      toast.error(message);
    },
  });

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();

    if (rating === 0) {
      toast.error('Please select a rating');
      return;
    }

    if (comment.length > 500) {
      toast.error('Comment must be 500 characters or less');
      return;
    }

    createMutation.mutate({
      reviewed_userid: reviewedUserId,
      listing_id: listingId,
      rating,
      comment: comment.trim() || undefined,
    });
  };

  return (
    <form onSubmit={handleSubmit} className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
      <h3 className="text-lg font-semibold text-gray-900 mb-4">
        Leave a Review
      </h3>

      <div className="mb-4">
        <label className="block text-sm font-medium text-gray-700 mb-2">
          Rating <span className="text-red-500">*</span>
        </label>
        <StarRating
          rating={rating}
          onRatingChange={setRating}
          size="lg"
        />
      </div>

      <div className="mb-4">
        <label htmlFor="comment" className="block text-sm font-medium text-gray-700 mb-2">
          Comment (Optional)
        </label>
        <textarea
          id="comment"
          value={comment}
          onChange={(e) => setComment(e.target.value)}
          placeholder="Share your experience with this seller..."
          rows={4}
          maxLength={500}
          className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
        />
        <div className="text-xs text-gray-500 mt-1 text-right">
          {comment.length}/500
        </div>
      </div>

      <button
        type="submit"
        disabled={createMutation.isPending || rating === 0}
        className="btn btn-primary w-full disabled:opacity-50 disabled:cursor-not-allowed"
      >
        {createMutation.isPending ? 'Submitting...' : 'Submit Review'}
      </button>
    </form>
  );
}
