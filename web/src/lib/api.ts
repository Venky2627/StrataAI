export interface ChatMessage {
  role: 'user' | 'assistant';
  content: string;
}

export interface ChatResponse {
  response: string;
  sources?: string[];
}

const API_BASE_URL = 'http://localhost:8000/api';

export async function sendChatMessage(message: string, history: ChatMessage[] = []): Promise<ChatResponse> {
  const response = await fetch(`${API_BASE_URL}/chat`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      message,
      history,
    }),
  });

  if (!response.ok) {
    throw new Error('Failed to send message to StrataAI Engine');
  }

  return response.json();
}
