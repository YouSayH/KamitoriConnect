"use client"

import { useEffect, useState } from 'react';
import Link from 'next/link';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import api from '@/lib/api';

interface Shop {
    id: number;
    name: string;
    category: string;
    description: string;
    map_url?: string;
}

export default function AdminDashboard() {
    const [shops, setShops] = useState<Shop[]>([]);

    useEffect(() => {
        fetchShops();
    }, []);

    const fetchShops = async () => {
        try {
            const res = await api.get('/shops');
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

            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                {shops.map((shop) => (
                    <Card key={shop.id}>
                        <CardHeader>
                            <CardTitle>{shop.name}</CardTitle>
                        </CardHeader>
                        <CardContent>
                            <p className="text-sm text-gray-500 mb-2">{shop.category}</p>
                            {shop.map_url && (
                                <a 
                                    href={shop.map_url} 
                                    target="_blank" 
                                    rel="noopener noreferrer"
                                    className="text-xs text-blue-500 hover:underline mb-2 block"
                                >
                                    📍 Google Map
                                </a>
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
