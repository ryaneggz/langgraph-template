import apiClient from '../lib/utils/apiClient';

export const listTools = async () => {
  const response = await apiClient.get('/tools');
  return response.data;
};