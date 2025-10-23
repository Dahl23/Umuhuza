import apiClient from './client';
import type { DealerApplication, DealerApplicationCreateData } from '../types';

export const dealerApplicationsApi = {
  // Submit dealer application
  create: async (data: DealerApplicationCreateData): Promise<{ message: string; application: DealerApplication }> => {
    const response = await apiClient.post('/dealer-applications/create/', data);
    return response.data;
  },

  // Get user's dealer application status
  getStatus: async (): Promise<DealerApplication | { message: string; has_application: false }> => {
    const response = await apiClient.get('/dealer-applications/status/');
    return response.data;
  },

  // Upload dealer documents
  uploadDocument: async (docType: string, fileUrl: string): Promise<{ message: string; document: any }> => {
    const response = await apiClient.post('/dealer-applications/documents/', {
      doc_type: docType,
      file_url: fileUrl,
    });
    return response.data;
  },
};
