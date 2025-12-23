"use client"

import { useState, useRef, useEffect } from 'react';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Card, CardContent, CardFooter, CardHeader, CardTitle } from '@/components/ui/card';
import { ScrollArea } from '@/components/ui/scroll-area';
import { Avatar, AvatarFallback, AvatarImage } from '@/components/ui/avatar';
import api from '@/lib/api';
import { Send, User, Bot } from 'lucide-react';

interface Message {
    role: 'user' | 'bot';
    content: string;
}

export default function ChatPage() {
    const [messages, setMessages] = useState<Message[]>([
        { role: 'bot', content: 'こんにちは！上通商栄会へようこそ。おすすめのお店や観光スポットについて何でも聞いてください！' }
    ]);
    const [input, setInput] = useState('');
    const [loading, setLoading] = useState(false);
    const scrollRef = useRef<HTMLDivElement>(null);

    const sendMessage = async () => {
        if (!input.trim() || loading) return;

        const userMsg = input;
        setMessages(prev => [...prev, { role: 'user', content: userMsg }]);
        setInput('');
        setLoading(true);

        try {
            const res = await api.post('/chat', { message: userMsg });
            setMessages(prev => [...prev, { role: 'bot', content: res.data.response }]);
        } catch (error) {
            console.error("Chat error", error);
            setMessages(prev => [...prev, { role: 'bot', content: 'すみません、エラーが発生しました。' }]);
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="flex flex-col h-screen bg-gray-50 p-4 md:p-8">
            <Card className="flex-1 flex flex-col max-w-2xl mx-auto w-full shadow-lg border-none">
                <CardHeader className="border-b bg-white rounded-t-lg">
                    <CardTitle className="flex items-center gap-2">
                        <Bot className="w-6 h-6 text-blue-500" />
                        Kamitori AI Concierge
                    </CardTitle>
                </CardHeader>

                <CardContent className="flex-1 p-0 overflow-hidden relative">
                    {/* ScrollArea creates a wrapper. We need to ensure it takes full height. */}
                    <div className="h-[60vh] md:h-[70vh] overflow-y-auto p-4 space-y-4" ref={scrollRef}>
                        {messages.map((msg, idx) => (
                            <div key={idx} className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}>
                                <div className={`flex gap-2 max-w-[80%] ${msg.role === 'user' ? 'flex-row-reverse' : 'flex-row'}`}>
                                    <Avatar className="w-8 h-8">
                                        <AvatarFallback className={msg.role === 'user' ? 'bg-green-100 text-green-700' : 'bg-blue-100 text-blue-700'}>
                                            {msg.role === 'user' ? <User size={16} /> : <Bot size={16} />}
                                        </AvatarFallback>
                                    </Avatar>
                                    <div className={`p-3 rounded-2xl text-sm ${msg.role === 'user' ? 'bg-green-500 text-white rounded-tr-none' : 'bg-gray-100 text-gray-800 rounded-tl-none border'}`}>
                                        {msg.content}
                                    </div>
                                </div>
                            </div>
                        ))}
                        {loading && (
                            <div className="flex justify-start">
                                <div className="bg-gray-100 p-3 rounded-2xl rounded-tl-none border text-sm text-gray-500">
                                    Writing...
                                </div>
                            </div>
                        )}
                    </div>
                </CardContent>

                <CardFooter className="p-4 bg-white border-t rounded-b-lg">
                    <div className="flex w-full gap-2">
                        <Input
                            placeholder="Type your message..."
                            value={input}
                            onChange={(e) => setInput(e.target.value)}
                            onKeyDown={(e) => e.key === 'Enter' && sendMessage()}
                            disabled={loading}
                            className="flex-1"
                        />
                        <Button onClick={sendMessage} disabled={loading} size="icon">
                            <Send className="w-4 h-4" />
                        </Button>
                    </div>
                </CardFooter>
            </Card>
        </div>
    );
}
