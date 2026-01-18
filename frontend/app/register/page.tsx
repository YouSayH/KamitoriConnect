"use client"

import { useState, useEffect } from 'react';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Card, CardContent, CardHeader, CardTitle, CardFooter } from '@/components/ui/card';
import { Label } from '@/components/ui/label';
import api from '@/lib/api';
import { useAuth } from '@/context/AuthContext';
import Link from 'next/link';

export default function RegisterPage() {
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [inviteCode, setInviteCode] = useState('');
    
    // 店舗情報用のState
    const [shopMode, setShopMode] = useState<'new' | 'existing'>('new');
    const [shopName, setShopName] = useState('');
    const [selectedShopId, setSelectedShopId] = useState('');
    const [unclaimedShops, setUnclaimedShops] = useState<{id: number, name: string}[]>([]);

    const [error, setError] = useState('');
    const { login } = useAuth();
    const [loading, setLoading] = useState(false);

    // 画面読み込み時に「オーナー不在の店舗」を取得
    useEffect(() => {
        const fetchUnclaimedShops = async () => {
            console.log("Fetching unclaimed shops...");
            try {
                const res = await api.get('/shops/unclaimed');
                console.log("Unclaimed shops:", res.data);
                setUnclaimedShops(res.data);
            } catch (err) {
                console.error("Failed to fetch shops", err);
            }
        };
        fetchUnclaimedShops();
    }, []);

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        console.log("Submit button clicked");
        setError('');
        setLoading(true);

        // 基本情報
        const payload: any = { 
            email, 
            password, 
            invite_code: inviteCode 
        };

        // 店舗情報の追加（モードに応じて）
        if (shopMode === 'new' && shopName) {
            payload.shop_name = shopName;
        } else if (shopMode === 'existing' && selectedShopId) {
            payload.existing_shop_id = parseInt(selectedShopId);
        }

        console.log("Sending payload:", payload);

        try {
            console.log("Calling API...");
            const res = await api.post('/auth/register', payload);
            console.log("API Response:", res);
            login(res.data.access_token);
        } catch (err: any) {
            console.error("API Error details:", err);
            if (err.response && err.response.status === 400) {
                const detail = err.response.data.detail;
                
                if (detail === "Invalid invitation code") {
                    setError('招待コードが間違っています。');
                } else if (detail === "Email already registered") {
                    setError('このメールアドレスは既に登録されています。');
                } else if (typeof detail === 'string' && detail.includes("Shop information")) {
                    setError('店舗情報の入力が必要です（店舗オーナーの場合）。');
                } else {
                    setError(detail || '登録に失敗しました。入力内容を確認してください。');
                }
            } else {
                setError('登録処理に失敗しました。サーバーエラーの可能性があります。');
            }
        } finally {
            console.log("Setting loading to false");
            setLoading(false);
        }
    };

    return (
        <div className="flex items-center justify-center min-h-[80vh] py-10">
            <Card className="w-full max-w-md">
                <CardHeader>
                    <CardTitle className="text-2xl text-center">Create Account</CardTitle>
                </CardHeader>
                <CardContent>
                    <form onSubmit={handleSubmit} className="space-y-4">
                        <div className="space-y-2">
                            <Label htmlFor="email">Email</Label>
                            <Input
                                id="email"
                                type="email"
                                value={email}
                                onChange={(e) => setEmail(e.target.value)}
                                required
                            />
                        </div>
                        <div className="space-y-2">
                            <Label htmlFor="password">Password</Label>
                            <Input
                                id="password"
                                type="password"
                                value={password}
                                onChange={(e) => setPassword(e.target.value)}
                                required
                            />
                        </div>
                        <div className="space-y-2">
                            <Label htmlFor="inviteCode">招待コード</Label>
                            <Input
                                id="inviteCode"
                                type="text"
                                placeholder="配布されたコードを入力してください"
                                value={inviteCode}
                                onChange={(e) => setInviteCode(e.target.value)}
                                required
                            />
                        </div>

                        {/* 店舗情報入力セクション */}
                        <div className="pt-4 border-t space-y-3">
                            <Label>店舗情報 (オーナー登録のみ)</Label>
                            
                            {/* 簡易タブ切り替え */}
                            <div className="flex space-x-2 mb-2">
                                <Button 
                                    type="button" 
                                    variant={shopMode === 'new' ? "default" : "outline"}
                                    onClick={() => setShopMode('new')}
                                    className="flex-1 text-xs"
                                >
                                    新規店舗を作成
                                </Button>
                                <Button 
                                    type="button" 
                                    variant={shopMode === 'existing' ? "default" : "outline"}
                                    onClick={() => setShopMode('existing')}
                                    className="flex-1 text-xs"
                                >
                                    既存店舗に参加
                                </Button>
                            </div>

                            {shopMode === 'new' ? (
                                <div className="space-y-2">
                                    <Input
                                        placeholder="新しい店舗の名前"
                                        value={shopName}
                                        onChange={(e) => setShopName(e.target.value)}
                                    />
                                </div>
                            ) : (
                                <div className="space-y-2">
                                    <select
                                        className="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50"
                                        value={selectedShopId}
                                        onChange={(e) => setSelectedShopId(e.target.value)}
                                    >
                                        <option value="">店舗を選択してください</option>
                                        {unclaimedShops.map((shop) => (
                                            <option key={shop.id} value={shop.id}>
                                                {shop.name}
                                            </option>
                                        ))}
                                    </select>
                                    {unclaimedShops.length === 0 && (
                                        <p className="text-xs text-yellow-600">
                                            ※ 現在、参加可能な店舗はありません。
                                        </p>
                                    )}
                                </div>
                            )}
                            <p className="text-xs text-gray-400">
                                ※ 管理者コードを使用する場合、この項目は無視されます。
                            </p>
                        </div>

                        {error && <p className="text-red-500 text-sm">{error}</p>}
                        <Button type="submit" className="w-full" disabled={loading}>
                            {loading ? 'Creating Account...' : 'Register'}
                        </Button>
                    </form>
                </CardContent>
                <CardFooter className="justify-center">
                    <p className="text-sm text-gray-500">
                        Already have an account? <Link href="/login" className="text-blue-500 hover:underline">Login</Link>
                    </p>
                </CardFooter>
            </Card>
        </div>
    );
}