import { API_ENDPOINTS } from './client';
import type { ChatRequest } from '@/types/api';

export type SSEEventType = 'content' | 'done' | 'error';

export type SSEEvent = {
  type: SSEEventType;
  content?: string;
  error?: string;
};

export async function* sendMessage(message: string): AsyncGenerator<string> {
  const response = await fetch(API_ENDPOINTS.CHAT_STREAM, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ message } as ChatRequest),
  });

  if (!response.ok) {
    throw new Error(`HTTP ${response.status}: ${response.statusText}`);
  }

  const reader = response.body?.getReader();
  const decoder = new TextDecoder();

  if (!reader) {
    throw new Error('Response body is not readable');
  }

  try {
    while (true) {
      const { done, value } = await reader.read();

      if (done) break;

      const chunk = decoder.decode(value, { stream: true });
      const lines = chunk.split('\n');

      for (const line of lines) {
        if (line.startsWith('data: ')) {
          const data = line.slice(6);

          try {
            const event: SSEEvent = JSON.parse(data);

            if (event.type === 'content' && event.content) {
              yield event.content;
            } else if (event.type === 'error') {
              throw new Error(event.error || 'Stream error');
            } else if (event.type === 'done') {
              return;
            }
          } catch (e) {
            console.error('Failed to parse SSE event:', data, e);
          }
        }
      }
    }
  } finally {
    reader.releaseLock();
  }
}

export async function resetChat(): Promise<void> {
  const response = await fetch(API_ENDPOINTS.CHAT_RESET, {
    method: 'POST',
  });

  if (!response.ok) {
    throw new Error(`Failed to reset chat: ${response.statusText}`);
  }
}
