import apiClient from './client';
import type {
  Payment,
  PaymentInitiateData,
  PaymentInitiateResponse,
  PaymentVerifyData,
  PricingPlan,
} from '../types';

export const paymentsApi = {
  // Initiate payment for a pricing plan
  initiate: async (data: PaymentInitiateData): Promise<PaymentInitiateResponse> => {
    const response = await apiClient.post('/payments/initiate/', data);
    return response.data;
  },

  // Verify payment (for testing - in production this is done via webhook)
  verify: async (data: PaymentVerifyData): Promise<{ message: string; payment: Payment }> => {
    const response = await apiClient.post('/payments/verify/', data);
    return response.data;
  },

  // Get payment history for logged-in user
  getHistory: async (): Promise<Payment[]> => {
    const response = await apiClient.get('/payments/history/');
    return response.data;
  },

  // Get single payment details
  getById: async (paymentId: string): Promise<Payment> => {
    const response = await apiClient.get(`/payments/${paymentId}/`);
    return response.data;
  },
};

export const pricingPlansApi = {
  // Get all active pricing plans
  getAll: async (): Promise<PricingPlan[]> => {
    const response = await apiClient.get('/pricing-plans/');
    return response.data;
  },

  // Get pricing plans by category
  getByCategory: async (category: 'all' | 'real_estate' | 'vehicle'): Promise<PricingPlan[]> => {
    const response = await apiClient.get(`/pricing-plans/?category=${category}`);
    return response.data;
  },

  // Get single pricing plan
  getById: async (pricingId: number): Promise<PricingPlan> => {
    const response = await apiClient.get(`/pricing-plans/${pricingId}/`);
    return response.data;
  },
};
