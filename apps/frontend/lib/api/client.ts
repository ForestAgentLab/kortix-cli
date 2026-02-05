const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';
const API_VERSION = process.env.NEXT_PUBLIC_API_VERSION || 'v1';

export const API_ENDPOINTS = {
  CHAT_STREAM: `${API_BASE_URL}/${API_VERSION}/chat`,
  CHAT_COMPLETION: `${API_BASE_URL}/${API_VERSION}/chat/completion`,
  CHAT_RESET: `${API_BASE_URL}/${API_VERSION}/chat/reset`,
  HISTORY: `${API_BASE_URL}/${API_VERSION}/history`,
  HISTORY_SAVE: `${API_BASE_URL}/${API_VERSION}/history/save`,
  HISTORY_LOAD: `${API_BASE_URL}/${API_VERSION}/history/load`,
  TOOLS: `${API_BASE_URL}/${API_VERSION}/tools`,
  HEALTH: `${API_BASE_URL}/health`,
};

export async function fetchAPI(url: string, options?: RequestInit) {
  const response = await fetch(url, {
    ...options,
    headers: {
      'Content-Type': 'application/json',
      ...options?.headers,
    },
  });

  if (!response.ok) {
    const error = await response.json().catch(() => ({ detail: 'Unknown error' }));
    throw new Error(error.detail || `HTTP ${response.status}`);
  }

  return response.json();
}
