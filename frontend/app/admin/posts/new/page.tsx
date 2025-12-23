"use client"

import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Textarea } from '@/components/ui/textarea';
import { Label } from '@/components/ui/label';
// import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select'; // Select isn't installed yet? 
// I didn't install Select in the shadcn command. I'll use standard select for now or install select.
// Or just basic select. I'll use basic HTML select for reliability in this step unless I add `select`.
// I'll stick to HTML select for now to avoid errors if I missed installing `select`.
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/card';
import api from '@/lib/api';

export default function CreatePostPage() {
    const router = useRouter();
    const [shops, setShops] = useState<any[]>([]);
    const [selectedShop, setSelectedShop] = useState('');
    const [text, setText] = useState('');
    const [image, setImage] = useState<File | null>(null);
    const [loading, setLoading] = useState(false);
    const [preview, setPreview] = useState<string | null>(null);

    useEffect(() => {
        // Fetch shops for selection
        api.get('/shops').then(res => setShops(res.data));
    }, []);

    const handleImageChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        if (e.target.files && e.target.files[0]) {
            const file = e.target.files[0];
            setImage(file);
            setPreview(URL.createObjectURL(file));
        }
    };

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        if (!selectedShop || !text || !image) return;

        setLoading(true);
        const formData = new FormData();
        formData.append('shop_id', selectedShop);
        formData.append('text', text);
        formData.append('image', image);

        try {
            await api.post('/posts', formData, {
                headers: {
                    'Content-Type': 'multipart/form-data',
                },
            });
            alert('AIによる記事作成と翻訳が完了しました！');
            router.push('/admin'); // or /
        } catch (error) {
            console.error("Failed to create post", error);
            alert('記事の作成に失敗しました。');
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="container mx-auto p-8 max-w-2xl">

            <section className="mb-12 text-center">
                <h2 className="text-3xl font-extrabold text-gray-900 mb-4">New Post</h2>
                <p className="text-gray-600 max-w-xl mx-auto">
                    一枚の写真、一つの言葉が、誰かの「行きたい」に変わります。 あなたのお店の素晴らしさを世界中に発信して、ブランドのファンをここから増やしていきましょう。
                </p>
            </section>

            <Card>
                <CardHeader>
                    <CardTitle>AI 記事作成</CardTitle>
                </CardHeader>
                <CardContent>
                    <form onSubmit={handleSubmit} className="space-y-6">

                        <div className="space-y-2">
                            <Label>店舗</Label>
                            <select
                                className="w-full p-2 border rounded-md"
                                value={selectedShop}
                                onChange={(e) => setSelectedShop(e.target.value)}
                                required
                            >
                                <option value="">店舗を選択してください...</option>
                                {shops.map(shop => (
                                    <option key={shop.id} value={shop.id}>{shop.name}</option>
                                ))}
                            </select>
                        </div>

                        <div className="space-y-2">
                            <Label>一言コメント</Label>
                            <Textarea
                                placeholder="今日は何が特別ですか？ (例: 期間限定の新作が出ました！)"
                                value={text}
                                onChange={(e) => setText(e.target.value)}
                                required
                            />
                        </div>

                        <div className="space-y-2">
                            <Label>写真</Label>
                            <Input type="file" accept="image/*" onChange={handleImageChange} required />
                            {preview && (
                                <div className="mt-4">
                                    <img src={preview} alt="Preview" className="max-h-64 rounded-md object-cover" />
                                </div>
                            )}
                        </div>

                        <Button type="submit" className="w-full" disabled={loading}>
                            {loading ? 'AIが生成中...' : '記事を作成・翻訳する'}
                        </Button>
                    </form>
                </CardContent>
            </Card>
        </div>
    );
}
