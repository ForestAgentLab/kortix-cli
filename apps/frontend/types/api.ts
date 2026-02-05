export type Message = {
  role: 'user' | 'assistant' | 'system' | 'tool';
  content: string;
  timestamp?: string;
  tool_calls?: any[];
  tool_call_id?: string;
  name?: string;
}

export type Tool = {
  name: string;
  description: string;
  functions: FunctionDefinition[];
}

export type FunctionDefinition = {
  name: string;
  description: string;
  parameters: Record<string, any>;
}

export type ChatRequest = {
  message: string;
  stream?: boolean;
}

export type ChatResponse = {
  content: string;
  tool_calls?: any[];
  timestamp: string;
}

export type HistoryResponse = {
  messages: Message[];
  total: number;
}
