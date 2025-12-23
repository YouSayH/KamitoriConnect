"use client"

import { useAuth } from '@/context/AuthContext';
import { useRouter } from 'next/navigation';
import { useEffect } from 'react';

export default function AdminLayout({
    children,
}: {
    children: React.ReactNode;
}) {
    const { isAuthenticated, token } = useAuth();
    const router = useRouter();

    useEffect(() => {
        // Simple check. Ideally we verify token validity.
        // Since AuthContext inits from localStorage in useEffect, there might be a split second of "not authenticated" initially.
        // But for this simple app, we can wait or redirect.
        // A better approach is to have a loading state in AuthContext.
        // Let's assume initialized by the time this runs if wrapped high enough or use a timeout.

        // Actually, AuthContext initial check might be async or delayed in useEffect.
        // We will just check token directly from localStorage here to be faster/safer for redirection on initial load
        const storedToken = localStorage.getItem('token');
        if (!storedToken) {
            router.push('/login');
        }
    }, [router]);

    return (
        <>
            {children}
        </>
    );
}
