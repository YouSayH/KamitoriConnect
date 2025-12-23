"use client"

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Textarea } from '@/components/ui/textarea';
import { Label } from '@/components/ui/label';
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/card';
import api from '@/lib/api';

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

                        <div className="space-y-2">
                            <Label htmlFor="map_url">Google Map URL</Label>
                            <Input 
                                id="map_url" 
                                name="map_url" 
                                placeholder="https://maps.app.goo.gl/..." 
                                value={formData.map_url} 
                                onChange={handleChange} 
                            />
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
