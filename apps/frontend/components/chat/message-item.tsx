'use client';

import { cn } from '@/lib/utils';
import type { Message } from '@/types/api';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';

interface MessageItemProps {
  message: Message;
  isStreaming?: boolean;
}

export function MessageItem({ message, isStreaming }: MessageItemProps) {
  const isUser = message.role === 'user';

  return (
    <div
      className={cn(
        'flex w-full py-6 px-4',
        isUser ? 'bg-background' : 'bg-muted/30'
      )}
    >
      <div className="mx-auto w-full max-w-4xl">
        <div className="flex gap-4">
          {/* Avatar */}
          <div
            className={cn(
              'flex h-8 w-8 shrink-0 select-none items-center justify-center rounded-md border',
              isUser
                ? 'bg-primary text-primary-foreground'
                : 'bg-secondary text-secondary-foreground'
            )}
          >
            {isUser ? '你' : 'AI'}
          </div>

          {/* Content */}
          <div className={cn(
            'flex-1 space-y-2 overflow-hidden',
            isStreaming && 'stream-fade-in'
          )}>
            {isUser ? (
              <div className="prose prose-sm dark:prose-invert max-w-none">
                <p className="whitespace-pre-wrap">{message.content}</p>
              </div>
            ) : (
              <div className="prose prose-sm dark:prose-invert max-w-none">
                <ReactMarkdown
                  remarkPlugins={[remarkGfm]}
                  components={{
                    code: ({ node, inline, className, children, ...props }: any) => {
                      const match = /language-(\w+)/.exec(className || '');
                      return !inline ? (
                        <pre className="overflow-x-auto rounded-md bg-muted p-4">
                          <code className={className} {...props}>
                            {children}
                          </code>
                        </pre>
                      ) : (
                        <code className="rounded bg-muted px-1 py-0.5" {...props}>
                          {children}
                        </code>
                      );
                    },
                  }}
                >
                  {message.content}
                </ReactMarkdown>
              </div>
            )}

            {/* Timestamp */}
            {message.timestamp && (
              <p className="text-xs text-muted-foreground">
                {new Date(message.timestamp).toLocaleTimeString('zh-CN')}
              </p>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
