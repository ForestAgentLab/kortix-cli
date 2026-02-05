'use client';

import { useEffect, useRef } from 'react';
import { ScrollArea } from '@/components/ui/scroll-area';
import { MessageItem } from './message-item';
import type { Message } from '@/types/api';

interface MessageListProps {
  messages: Message[];
  streamingMessage?: string;
}

export function MessageList({ messages, streamingMessage }: MessageListProps) {
  const scrollRef = useRef<HTMLDivElement>(null);
  const bottomRef = useRef<HTMLDivElement>(null);

  // Auto-scroll to bottom when new messages arrive
  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages.length, streamingMessage]);

  return (
    <div ref={scrollRef} className="flex-1 overflow-hidden">
      <ScrollArea className="h-full">
        <div className="flex flex-col">
          {messages.length === 0 && !streamingMessage ? (
            <div className="flex h-full items-center justify-center p-8">
              <div className="text-center space-y-2">
                <h2 className="text-2xl font-semibold">欢迎使用 Kortix AI</h2>
                <p className="text-muted-foreground">
                  输入消息开始对话
                </p>
              </div>
            </div>
          ) : (
            <>
              {messages.map((message, index) => (
                <MessageItem
                  key={index}
                  message={message}
                />
              ))}

              {streamingMessage && (
                <MessageItem
                  message={{
                    role: 'assistant',
                    content: streamingMessage,
                  }}
                  isStreaming={true}
                />
              )}
            </>
          )}
          <div ref={bottomRef} />
        </div>
      </ScrollArea>
    </div>
  );
}
