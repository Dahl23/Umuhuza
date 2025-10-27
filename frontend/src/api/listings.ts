import apiClient from './client';
import type { Listing, Category } from '../types';

interface ListingsParams {
  page?: number;
  page_size?: number;
  category?: number;
  min_price?: number;
  max_price?: number;
  location?: string;
  search?: string;
  ordering?: string;
  is_featured?: boolean;
}

interface ListingsResponse {
  count: number;
  next: string | null;
  previous: string | null;
  results: Listing[];
}

export const listingsApi = {
  // Get all listings with filters
  getAll: async (params?: ListingsParams): Promise<ListingsResponse> => {
    const response = await apiClient.get('/listings/', { params });
    return response.data;
  },

  // Get single listing
  getById: async (id: number): Promise<Listing> => {
    const response = await apiClient.get(`/listings/${id}/`);
    return response.data;
  },

  // Get featured listings
  getFeatured: async (): Promise<Listing[]> => {
    const response = await apiClient.get('/listings/featured/');
    return response.data;
  },

  // Get similar listings
  getSimilar: async (id: number): Promise<Listing[]> => {
    const response = await apiClient.get(`/listings/${id}/similar/`);
    return response.data;
  },

  // Get user's listings
  getMyListings: async (): Promise<Listing[]> => {
    const response = await apiClient.get('/listings/my-listings/');
    return response.data;
  },

  // Create listing
  create: async (data: FormData): Promise<Listing> => {
    const response = await apiClient.post('/listings/create/', data, {
      headers: { 'Content-Type': 'multipart/form-data' },
    });
    return response.data.listing;
  },

  // Update listing
  update: async (id: number, data: Partial<Listing>): Promise<Listing> => {
    const response = await apiClient.put(`/listings/${id}/update/`, data);
    return response.data.listing;
  },

  // Update listing status
  updateStatus: async (id: number, status: 'active' | 'sold' | 'hidden'): Promise<Listing> => {
    const response = await apiClient.patch(`/listings/${id}/update-status/`, { status });
    return response.data.listing;
  },

  // Delete listing
  delete: async (id: number): Promise<void> => {
    await apiClient.delete(`/listings/${id}/delete/`);
  },

  // Get categories
  getCategories: async (): Promise<Category[]> => {
    const response = await apiClient.get('/categories/');
    return response.data;
  },

  // Toggle favorite
  toggleFavorite: async (listingId: number): Promise<{ is_favorited: boolean }> => {
    const response = await apiClient.post(`/favorites/${listingId}/toggle/`);
    return response.data;
  },

  // Get favorites
  getFavorites: async (): Promise<any[]> => {
    const response = await apiClient.get('/favorites/');
    return response.data;
  },

  // Get current subscription
  getCurrentSubscription: async (): Promise<any> => {
    const response = await apiClient.get('/subscription/current/');
    return response.data;
  },
};