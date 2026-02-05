import { API_ENDPOINTS, fetchAPI } from './client';
import type { HistoryResponse } from '@/types/api';

export async function getHistory(limit = 50): Promise<HistoryResponse> {
  return fetchAPI(`${API_ENDPOINTS.HISTORY}?limit=${limit}`);
}

export async function saveHistory(): Promise<void> {
  await fetchAPI(API_ENDPOINTS.HISTORY_SAVE, {
    method: 'POST',
  });
}

export async function clearHistory(): Promise<void> {
  await fetchAPI(API_ENDPOINTS.HISTORY, {
    method: 'DELETE',
  });
}
