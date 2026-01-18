"use client"

import { useEffect, useState } from 'react';
import Link from 'next/link';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import api from '@/lib/api';
import { MapPinned } from 'lucide-react';

interface Shop {
    id: number;
    name: string;
    category: string;
    description: string;
    map_url?: string;
}

export default function AdminDashboard() {
    const [shops, setShops] = useState<Shop[]>([]);

    const getEmbedUrl = (url: string) => {
        if (!url) return null;
        if (url.includes("output=embed")) return url;
        // URLエンコード処理を修正
        return `https://maps.google.com/maps?q=${encodeURIComponent(url)}&output=embed`;
    };

    useEffect(() => {
        fetchShops();
    }, []);

    const fetchShops = async () => {
        try {
            // [変更] 管理対象の店舗のみを取得するエンドポイントに変更
            const res = await api.get('/shops/managed');
            setShops(res.data);
        } catch (error) {
            console.error("Failed to fetch shops", error);
        }
    };

    return (
        <div className="container mx-auto p-8">
            <div className="flex justify-between items-center mb-8">
                <h1 className="text-3xl font-bold">管理ダッシュボード</h1>
                <div className="space-x-4">
                    <Link href="/admin/shops/new">
                        <Button>+ 店舗を登録</Button>
                    </Link>
                    <Link href="/admin/posts/new">
                        <Button variant="secondary">+ AI記事作成</Button>
                    </Link>
                </div>
            </div>

            {shops.length === 0 && (
                <div className="text-center py-10 text-gray-500 bg-gray-50 rounded-lg">
                    <p>管理対象の店舗がありません。</p>
                    <p className="text-sm mt-2">新しい店舗を登録するか、管理者に問い合わせてください。</p>
                </div>
            )}

            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                {shops.map((shop) => (
                    <Card key={shop.id}>
                        <CardHeader>
                            <CardTitle>{shop.name}</CardTitle>
                        </CardHeader>
                        <CardContent>
                            <p className="text-sm text-gray-500 mb-2">{shop.category}</p>

                            {shop.map_url && (
                                <div className="relative group mb-2"> {/* relative group でホバーを検知 */}
                                    <a 
                                        href={shop.map_url} 
                                        target="_blank" 
                                        rel="noopener noreferrer"
                                        className="text-xs text-blue-500 hover:underline flex items-center gap-1"
                                    >
                                        <MapPinned size={14} /> Google Map
                                    </a>
                                    
                                    {/* ホバー時に浮き出るプレビュー窓 (z-50で最前面に表示) */}
                                    <div className="absolute left-0 top-full mt-1 z-50 w-64 hidden group-hover:block transition-all drop-shadow-lg">
                                        <div className="bg-white border rounded-md overflow-hidden h-48 w-full">
                                            <iframe
                                                width="100%"
                                                height="100%"
                                                style={{ border: 0 }}
                                                src={getEmbedUrl(shop.map_url) || ""}
                                                allowFullScreen
                                                loading="lazy"
                                            ></iframe>
                                        </div>
                                    </div>
                                </div>
                            )}

                            <p className="line-clamp-3 mb-4">{shop.description}</p>
                            <div className="flex justify-end space-x-2">
                                <Link href={`/admin/shops/${shop.id}`}>
                                    <Button variant="outline" size="sm">編集</Button>
                                </Link>
                            </div>
                        </CardContent>
                    </Card>
                ))}
            </div>
        </div>
    );
}