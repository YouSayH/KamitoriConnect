"use client"

import { useState, useEffect, use } from 'react';
import { useRouter } from 'next/navigation';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Textarea } from '@/components/ui/textarea';
import { Label } from '@/components/ui/label';
import { Card, CardHeader, CardTitle, CardContent, CardFooter } from '@/components/ui/card';
import api from '@/lib/api';

export default function EditShopPage({ params }: { params: Promise<{ id: string }> }) {
    const router = useRouter();
    // Unwrap params using React.use() or await in async component. 
    // Next.js 15 params is async.
    const { id } = use(params);

    const [formData, setFormData] = useState({
        name: '',
        description: '',
        location: '',
        category: ''
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
                        category: res.data.category || ''
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
