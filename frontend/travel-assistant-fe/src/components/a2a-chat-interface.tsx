import { useState, useRef, useEffect } from 'react';
import { Send, MessageCircle, Bot, User, Loader2, } from 'lucide-react';

// Mock A2A client implementation for demo
type Message = {
  id: string;
  role: 'user' | 'assistant' | 'system';
  content: string;
  timestamp: Date;
  isError?: boolean;
  isStreaming?: boolean;
};

class MockA2AClient {
  connected: boolean; 
  constructor() {
    this.connected = false;
  }

  async initialize() {
    // Simulate initialization delay
    await new Promise(resolve => setTimeout(resolve, 1000));
    this.connected = true;
    return { success: true, agentCard: 'Public Agent Card' };
  }

  async sendMessage(message: any) {
    // Simulate API call delay
    await new Promise(resolve => setTimeout(resolve, 500 + Math.random() * 1000));
    
    // Mock responses based on message content
    const responses = [
      "I'd be happy to help you with that request. Let me process the information.",
      "Based on your query, here are some suggestions I can provide.",
      "I understand you're looking for assistance. Let me work on that for you.",
      "That's an interesting question. Here's what I can tell you about it.",
      "I'll help you find the best solution for your needs."
    ];
    
    return {
      role: 'assistant',
      content: responses[Math.floor(Math.random() * responses.length)] + ` (Response to: "${message}")`,
      messageId: Math.random().toString(36).substr(2, 9)
    };
  }

  async *sendMessageStreaming(message: any) {
    const fullResponse = `I understand you're asking about: "${message}". Let me provide you with a comprehensive response that addresses your query in detail.`;
    const words = fullResponse.split(' ');
    
    for (let i = 0; i < words.length; i++) {
      await new Promise(resolve => setTimeout(resolve, 50 + Math.random() * 100));
      yield {
        role: 'assistant',
        content: words.slice(0, i + 1).join(' '),
        messageId: Math.random().toString(36).substr(2, 9),
        isComplete: i === words.length - 1
      };
    }
  }
}

const A2AChatInterface = () => {
  const [messages, setMessages] = useState<Message[]>([]);
  const [inputMessage, setInputMessage] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [isConnected, setIsConnected] = useState(false);
  const [connectionStatus, setConnectionStatus] = useState('disconnected');
  const [streamingMessageId, setStreamingMessageId] = useState<string>("");
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const inputRef = useRef<HTMLInputElement>(null);
  const clientRef = useRef<MockA2AClient | null>(null);

  // Initialize A2A client on component mount
  useEffect(() => {
    initializeClient();
  }, []);

  // Auto-scroll to bottom when new messages arrive
  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  const initializeClient = async () => {
    setConnectionStatus('connecting');
    try {
      clientRef.current = new MockA2AClient();
      const result = await clientRef.current.initialize();
      
      if (result.success) {
        setIsConnected(true);
        setConnectionStatus('connected');
        setMessages([{
          id: Date.now().toString(),
          role: 'system',
          content: `Connected to A2A Agent (${result.agentCard})`,
          timestamp: new Date()
        }]);
      }
    } catch (error: any) {
      setConnectionStatus('error');
      setMessages([{
        id: Date.now().toString(),
        role: 'system',
        content: `Connection failed: ${error.message}`,
        timestamp: new Date(),
        isError: true
      }]);
    }
  };

  const handleSendMessage = async (e: { preventDefault: () => void; } | undefined) => {
    if (e && e.preventDefault) e.preventDefault();
    if (!inputMessage.trim() || !isConnected || isLoading) return;

    const userMessage: Message = {
      id: Date.now().toString(),
      role: 'user',
      content: inputMessage.trim(),
      timestamp: new Date()
    };

    setMessages(prev => [...prev, userMessage]);
    setInputMessage('');
    setIsLoading(true);

    try {
      // Create placeholder for streaming response
      const assistantMessageId = (Date.now() + 1).toString();
      setStreamingMessageId(assistantMessageId);
      
      const assistantMessage: Message = {
        id: assistantMessageId,
        role: 'assistant',
        content: '',
        timestamp: new Date(),
        isStreaming: true
      };
      
      setMessages(prev => [...prev, assistantMessage]);

      // Use streaming response
      const stream = clientRef.current?.sendMessageStreaming(userMessage.content);
      if(stream){
        for await (const chunk of stream) {
          setMessages(prev => prev.map(msg => 
            msg.id === assistantMessageId 
              ? { ...msg, content: chunk.content, isStreaming: !chunk.isComplete }
              : msg
          ));
        }
        
      }

      setStreamingMessageId("");
    } catch (error: any) {
      setMessages(prev => [...prev, {
        id: (Date.now() + 1).toString(),
        role: 'system',
        content: `Error: ${error?.message}`,
        timestamp: new Date(),
        isError: true
      }]);
    } finally {
      setIsLoading(false);
    }
  };

  const getStatusColor = () => {
    switch (connectionStatus) {
      case 'connected': return 'text-green-500';
      case 'connecting': return 'text-yellow-500';
      case 'error': return 'text-red-500';
      default: return 'text-gray-500';
    }
  };

  const getStatusText = () => {
    switch (connectionStatus) {
      case 'connected': return 'Connected';
      case 'connecting': return 'Connecting...';
      case 'error': return 'Connection Error';
      default: return 'Disconnected';
    }
  };

  return (
    <div className="flex flex-col h-screen bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900">
      {/* Header */}
      <div className="bg-slate-800/80 backdrop-blur-sm border-b border-slate-700/50 p-4 shadow-lg">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-3">
            <div className="p-2 bg-blue-500/20 rounded-lg">
              <MessageCircle className="w-6 h-6 text-blue-400" />
            </div>
            <div>
              <h1 className="text-xl font-bold text-white">Travel Assistant</h1>
              {/* <p className="text-sm text-slate-400">Agent-to-Agent Communication</p> */}
            </div>
          </div>
          {/* <div className="flex items-center space-x-2">
            <div className={`w-2 h-2 rounded-full ${connectionStatus === 'connected' ? 'bg-green-500' : connectionStatus === 'connecting' ? 'bg-yellow-500' : 'bg-red-500'}`}></div>
            <span className={`text-sm font-medium ${getStatusColor()}`}>
              {getStatusText()}
            </span>
          </div> */}
        </div>
      </div>

      {/* Messages Container */}
      <div className="flex-1 overflow-y-auto p-4 space-y-4">
        {messages.length === 0 && (
          <div className="text-center text-slate-400 mt-20">
            <MessageCircle className="w-12 h-12 mx-auto mb-4 opacity-50" />
            <p className="text-lg font-medium">Welcome to A2A Chat</p>
            <p className="text-sm">Start a conversation with the agent</p>
          </div>
        )}

        {messages.map((message) => (
          <div
            key={message.id}
            className={`flex ${message.role === 'user' ? 'justify-end' : 'justify-start'} ${message.role === 'system' ? 'justify-center' : ''}`}
          >
            <div
              className={`max-w-xs lg:max-w-md xl:max-w-lg px-4 py-3 rounded-2xl ${
                message.role === 'user'
                  ? 'bg-blue-500 text-white ml-auto'
                  : message.role === 'system'
                  ? `bg-slate-700/50 text-slate-300 text-sm ${message.isError ? 'border border-red-500/30 text-red-300' : ''}`
                  : 'bg-slate-700/80 text-slate-100 border border-slate-600/30'
              } shadow-lg`}
            >
              {message.role !== 'system' && (
                <div className="flex items-center space-x-2 mb-2">
                  {message.role === 'user' ? (
                    <User className="w-4 h-4" />
                  ) : (
                    <Bot className="w-4 h-4 text-blue-400" />
                  )}
                  <span className="text-xs font-medium opacity-70">
                    {message.role === 'user' ? 'You' : 'Assistant'}
                  </span>
                  {message.isStreaming && (
                    <Loader2 className="w-3 h-3 animate-spin" />
                  )}
                </div>
              )}
              
              <p className="text-sm leading-relaxed">{message.content}</p>
              
              {message.role !== 'system' && (
                <div className="text-xs opacity-50 mt-2">
                  {message.timestamp.toLocaleTimeString()}
                </div>
              )}
            </div>
          </div>
        ))}
        
        <div ref={messagesEndRef} />
      </div>

      {/* Input Form */}
      <div className="bg-slate-800/80 backdrop-blur-sm border-t border-slate-700/50 p-4">
        <div className="flex space-x-3">
          <div className="flex-1 relative">
            <input
              ref={inputRef}
              type="text"
              value={inputMessage}
              onChange={(e) => setInputMessage(e.target.value)}
              onKeyPress={(e) => e.key === 'Enter' && handleSendMessage(e)}
              placeholder={isConnected ? "Type your message..." : "Waiting for connection..."}
              disabled={!isConnected || isLoading}
              className="w-full px-4 py-3 bg-slate-700/50 border border-slate-600/30 rounded-xl text-white placeholder-slate-400 focus:outline-none focus:ring-2 focus:ring-blue-500/50 focus:border-transparent disabled:opacity-50 disabled:cursor-not-allowed"
            />
          </div>
          
          <button
            type="button"
            onClick={handleSendMessage}
            disabled={!inputMessage.trim() || !isConnected || isLoading}
            className="px-6 py-3 bg-blue-500 hover:bg-blue-600 disabled:bg-slate-600 disabled:cursor-not-allowed text-white rounded-xl transition-colors duration-200 flex items-center space-x-2 shadow-lg"
          >
            {isLoading ? (
              <Loader2 className="w-4 h-4 animate-spin" />
            ) : (
              <Send className="w-4 h-4" />
            )}
            <span className="hidden sm:inline">Send</span>
          </button>
        </div>
        
        <div className="mt-2 text-xs text-slate-400 text-center">
          {isLoading ? 'Agent is typing...' : 'Press Enter to send message'}
        </div>
      </div>
    </div>
  );
};

export default A2AChatInterface;