'use client';

import { useState } from 'react';
import { MessageList } from './message-list';
import { MessageInput } from './message-input';
import { Button } from '@/components/ui/button';
import { RotateCcw, Loader2 } from 'lucide-react';
import { sendMessage, resetChat } from '@/lib/api/chat';
import type { Message } from '@/types/api';

export function ChatContainer() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [streamingMessage, setStreamingMessage] = useState('');
  const [isLoading, setIsLoading] = useState(false);

  const handleSendMessage = async (content: string) => {
    // Add user message
    const userMessage: Message = {
      role: 'user',
      content,
      timestamp: new Date().toISOString(),
    };

    setMessages(prev => [...prev, userMessage]);
    setIsLoading(true);
    setStreamingMessage('');

    try {
      // Stream assistant response
      let fullResponse = '';

      for await (const chunk of sendMessage(content)) {
        fullResponse += chunk;
        setStreamingMessage(fullResponse);
      }

      // Add completed assistant message
      const assistantMessage: Message = {
        role: 'assistant',
        content: fullResponse,
        timestamp: new Date().toISOString(),
      };

      setMessages(prev => [...prev, assistantMessage]);
      setStreamingMessage('');
    } catch (error) {
      console.error('Error sending message:', error);
      const errorMessage: Message = {
        role: 'assistant',
        content: `错误：${error instanceof Error ? error.message : '发送消息失败'}`,
        timestamp: new Date().toISOString(),
      };
      setMessages(prev => [...prev, errorMessage]);
      setStreamingMessage('');
    } finally {
      setIsLoading(false);
    }
  };

  const handleReset = async () => {
    try {
      await resetChat();
      setMessages([]);
      setStreamingMessage('');
    } catch (error) {
      console.error('Error resetting chat:', error);
    }
  };

  return (
    <div className="flex h-screen flex-col">
      {/* Header */}
      <div className="border-b bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60">
        <div className="flex h-14 items-center justify-between px-4">
          <h1 className="text-lg font-semibold">Kortix AI 助手</h1>
          <Button
            variant="outline"
            size="sm"
            onClick={handleReset}
            disabled={isLoading || (messages.length === 0 && !streamingMessage)}
          >
            <RotateCcw className="mr-2 h-4 w-4" />
            重置对话
          </Button>
        </div>
      </div>

      {/* Messages */}
      <MessageList
        messages={messages}
        streamingMessage={streamingMessage}
      />

      {/* Loading indicator */}
      {isLoading && !streamingMessage && (
        <div className="flex items-center justify-center py-4">
          <Loader2 className="h-6 w-6 animate-spin text-muted-foreground" />
          <span className="ml-2 text-sm text-muted-foreground">AI 正在思考...</span>
        </div>
      )}

      {/* Input */}
      <MessageInput
        onSendMessage={handleSendMessage}
        disabled={isLoading}
      />
    </div>
  );
}
