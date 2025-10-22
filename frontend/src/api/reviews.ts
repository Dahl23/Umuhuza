import apiClient from './client';
import type { Review, ReviewCreateData, ReviewsResponse } from '../types';

export const reviewsApi = {
  // Get reviews for a user
  getUserReviews: async (userId: number): Promise<ReviewsResponse> => {
    const response = await apiClient.get(`/reviews/user/${userId}/`);
    return response.data;
  },

  // Create a review
  create: async (data: ReviewCreateData): Promise<{ message: string; review: Review }> => {
    const response = await apiClient.post('/reviews/create/', data);
    return response.data;
  },
};
