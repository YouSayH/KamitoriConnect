"use client"

import { useState, useEffect, use } from 'react';
import { useRouter } from 'next/navigation';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Textarea } from '@/components/ui/textarea';
import { Label } from '@/components/ui/label';
import { Card, CardHeader, CardTitle, CardContent, CardFooter } from '@/components/ui/card';
import api from '@/lib/api';
import { MapPinned } from 'lucide-react';

export default function EditShopPage({ params }: { params: Promise<{ id: string }> }) {
    const router = useRouter();
    // Unwrap params using React.use() or await in async component. 
    // Next.js 15 params is async.
    const { id } = use(params);

    const [formData, setFormData] = useState({
        name: '',
        description: '',
        location: '',
        category: '',
        map_url: '',
        reservation_url: ''
    });
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        if (id) {
            api.get(`/shops/${id}`)
                .then(res => {
                    setFormData({
                        name: res.data.name,
                        description: res.data.description || '',
                        location: res.data.location || '',
                        category: res.data.category || '',
                        map_url: res.data.map_url || '',
                        reservation_url: res.data.reservation_url || ''
                    });
                    setLoading(false);
                })
                .catch(err => console.error(err));
        }
    }, [id]);

    const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
        setFormData({ ...formData, [e.target.name]: e.target.value });
    };

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        try {
            await api.put(`/shops/${id}`, formData);
            router.push('/admin');
        } catch (error) {
            console.error("Failed to update shop", error);
        }
    };
    const getEmbedUrl = (url: string) => {
        if (!url) return null;
        if (url.includes("output=embed")) return url;
        return `https://maps.google.com/maps?q=$0{encodeURIComponent(url)}&output=embed`;
    };

    const handleDelete = async () => {
        if (confirm('本当にこの店舗を削除してもよろしいですか？')) {
            try {
                await api.delete(`/shops/${id}`);
                router.push('/admin');
            } catch (error) {
                console.error("Failed to delete shop", error);
            }
        }
    };

    if (loading) return <div>Loading...</div>;

    return (
        <div className="container mx-auto p-8 max-w-2xl">
            <Card>
                <CardHeader>
                    <CardTitle>店舗情報の編集</CardTitle>
                </CardHeader>
                <CardContent>
                    <form onSubmit={handleSubmit} className="space-y-4">
                        <div className="space-y-2">
                            <Label htmlFor="name">店舗名</Label>
                            <Input id="name" name="name" value={formData.name} onChange={handleChange} required />
                        </div>

                        <div className="space-y-2">
                            <Label htmlFor="category">カテゴリ</Label>
                            <Input id="category" name="category" value={formData.category} onChange={handleChange} />
                        </div>

                        <div className="space-y-2">
                            <Label htmlFor="location">場所</Label>
                            <Input id="location" name="location" value={formData.location} onChange={handleChange} />
                        </div>

                        <div className="space-y-2 relative group">
                            <div className="flex items-center gap-2">
                                <Label htmlFor="map_url">Google Map URL</Label>
                                {formData.map_url && (
                                    <div className="flex items-center gap-1 text-xs text-blue-600 cursor-help font-medium border-b border-blue-600 border-dotted">
                                        <MapPinned size={14} />
                                        ホバーでプレビュー
                                    </div>
                                )}
                            </div>
                            <Input 
                                id="map_url" 
                                name="map_url" 
                                value={formData.map_url} 
                                onChange={handleChange} 
                                placeholder="住所またはURLを入力"
                            />
                            
                            {/* マウスホバー時のみ表示される絶対配置のプレビュー窓 */}
                            {formData.map_url && (
                                <div className="absolute left-0 top-full mt-2 z-50 w-full max-w-sm hidden group-hover:block transition-all duration-200">
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
                                value={formData.reservation_url} 
                                onChange={handleChange} 
                            />
                        </div>

                        <div className="space-y-2">
                            <Label htmlFor="description">説明文</Label>
                            <Textarea id="description" name="description" value={formData.description} onChange={handleChange} />
                        </div>

                        <Button type="submit" className="w-full">情報を更新</Button>
                    </form>
                </CardContent>
                <CardFooter className="justify-center border-t p-4">
                    <Button variant="destructive" onClick={handleDelete} className="w-full">店舗を削除</Button>
                </CardFooter>
            </Card>
        </div>
    );
}
