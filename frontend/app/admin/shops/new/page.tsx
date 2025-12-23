"use client"

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Textarea } from '@/components/ui/textarea';
import { Label } from '@/components/ui/label';
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/card';
import api from '@/lib/api';
import { MapPinned } from 'lucide-react';

export default function CreateShopPage() {
    const router = useRouter();
    const [formData, setFormData] = useState({
        name: '',
        description: '',
        location: '',
        category: '',
        map_url: '',
        reservation_url: ''
    });

    const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
        setFormData({ ...formData, [e.target.name]: e.target.value });
    };

    const getEmbedUrl = (url: string) => {
        if (!url) return null;
        if (url.includes("output=embed")) return url;
        // ${ } を使って正しく変数展開します
        return `https://maps.google.com/maps?q=$0{encodeURIComponent(url)}&output=embed`;
    };

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        try {
            await api.post('/shops', formData);
            router.push('/admin');
        } catch (error) {
            console.error("Failed to create shop", error);
        }
    };

    return (
        <div className="container mx-auto p-8 max-w-2xl">
            <Card>
                <CardHeader>
                    <CardTitle>新規店舗登録</CardTitle>
                </CardHeader>
                <CardContent>
                    <form onSubmit={handleSubmit} className="space-y-4">
                        <div className="space-y-2">
                            <Label htmlFor="name">店舗名</Label>
                            <Input id="name" name="name" value={formData.name} onChange={handleChange} required />
                        </div>

                        <div className="space-y-2">
                            <Label htmlFor="category">カテゴリ</Label>
                            <Input id="category" name="category" placeholder="例: ラーメン, カフェ, 雑貨" value={formData.category} onChange={handleChange} />
                        </div>

                        <div className="space-y-2">
                            <Label htmlFor="location">場所</Label>
                            <Input id="location" name="location" placeholder="例: 北エリア, 1F" value={formData.location} onChange={handleChange} />
                        </div>

                        <div className="space-y-2 relative group">
                            <div className="flex items-center gap-2">
                                <Label htmlFor="map_url">Google Map URL</Label>
                                {formData.map_url && (
                                    <div className="flex items-center gap-1 text-xs text-blue-600 cursor-help font-medium border-b border-blue-600 border-dotted">
                                        <MapPinned size={14} /> ホバーでプレビュー
                                    </div>
                                )}
                            </div>
                            <Input 
                                id="map_url" 
                                name="map_url" 
                                placeholder="住所やリンクを入力" 
                                value={formData.map_url} 
                                onChange={handleChange} 
                            />
                            
                            {/* 新規登録時もホバーで確認可能に */}
                            {formData.map_url && (
                                <div className="absolute left-0 top-full mt-2 z-50 w-full max-w-sm hidden group-hover:block transition-all">
                                    <div className="bg-white border rounded-lg shadow-2xl overflow-hidden h-64 w-full">
                                        <iframe
                                            width="100%"
                                            height="100%"
                                            style={{ border: 0 }}
                                            src={getEmbedUrl(formData.map_url) || ""}
                                            allowFullScreen
                                            loading="lazy"
                                        ></iframe>
                                    </div>
                                </div>
                            )}
                        </div>

                        <div className="space-y-2">
                            <Label htmlFor="reservation_url">予約サイト URL (任意)</Label>
                            <Input 
                                id="reservation_url" 
                                name="reservation_url" 
                                placeholder="https://tabelog.com/..." 
                                value={formData.reservation_url} 
                                onChange={handleChange} 
                            />
                        </div>

                        <div className="space-y-2">
                            <Label htmlFor="description">説明文</Label>
                            <Textarea id="description" name="description" value={formData.description} onChange={handleChange} />
                        </div>

                        <Button type="submit" className="w-full">店舗を登録</Button>
                    </form>
                </CardContent>
            </Card>
        </div>
    );
}
