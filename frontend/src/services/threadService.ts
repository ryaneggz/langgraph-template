import apiClient from '@/lib/utils/apiClient';

export const findThread = async (threadId: string) => {
  const response = await apiClient.get(`/thread/${threadId}`);
  return response.data;
};