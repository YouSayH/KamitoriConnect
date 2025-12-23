"use client"

import Link from 'next/link';
import { Button } from '@/components/ui/button';
import { MessageCircle, Settings, PenTool, Home, LogIn, LogOut } from 'lucide-react';
import { useAuth } from '@/context/AuthContext';

export default function Header() {
    const { isAuthenticated, logout } = useAuth();

    return (
        <header className="bg-white border-b sticky top-0 z-50 shadow-sm">
            <div className="container mx-auto px-4 py-3 flex justify-between items-center">
                <div className="flex items-center gap-6">
                    <Link href="/" className="flex items-center gap-2 hover:opacity-80 transition-opacity">
                        <h1 className="text-xl font-bold tracking-tight text-gray-900">Kamitori Connect</h1>
                    </Link>

                    {/* Desktop Navigation */}
                    <nav className="hidden md:flex gap-4">
                        <Link href="/" className="text-sm font-medium text-gray-600 hover:text-blue-600 flex items-center gap-1">
                            <Home size={16} /> ホーム
                        </Link>
                        <Link href="/chat" className="text-sm font-medium text-gray-600 hover:text-blue-600 flex items-center gap-1">
                            <MessageCircle size={16} /> AIコンシェルジュ
                        </Link>
                    </nav>
                </div>

                <div className="flex items-center gap-2">
                    {isAuthenticated ? (
                        <>
                            <Link href="/admin/posts/new">
                                <Button variant="ghost" size="sm" className="gap-2 text-gray-600">
                                    <PenTool size={16} /> <span className="hidden sm:inline">投稿</span>
                                </Button>
                            </Link>
                            <Link href="/admin">
                                <Button variant="outline" size="sm" className="gap-2">
                                    <Settings size={16} /> <span className="hidden sm:inline">管理者</span>
                                </Button>
                            </Link>
                            <Button variant="ghost" size="sm" onClick={logout} className="text-gray-500 hover:text-red-500">
                                <LogOut size={16} />
                            </Button>
                        </>
                    ) : (
                        <Link href="/login">
                            <Button variant="default" size="sm" className="gap-2">
                                <LogIn size={16} /> ログイン
                            </Button>
                        </Link>
                    )}
                </div>
            </div>
        </header>
    );
}
