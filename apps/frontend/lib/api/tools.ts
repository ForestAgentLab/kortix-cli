import { API_ENDPOINTS, fetchAPI } from './client';
import type { Tool } from '@/types/api';

export async function getTools(): Promise<{ tools: Tool[] }> {
  return fetchAPI(API_ENDPOINTS.TOOLS);
}

export async function getTool(name: string): Promise<Tool> {
  return fetchAPI(`${API_ENDPOINTS.TOOLS}/${name}`);
}
