"use client"

import React, { createContext, useState, useContext, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import api from '@/lib/api';

interface AuthContextType {
    token: string | null;
    login: (token: string) => void;
    logout: () => void;
    isAuthenticated: boolean;
}

const AuthContext = createContext<AuthContextType>({
    token: null,
    login: () => { },
    logout: () => { },
    isAuthenticated: false,
});

export const AuthProvider = ({ children }: { children: React.ReactNode }) => {
    const [token, setToken] = useState<string | null>(null);
    const [isAuthenticated, setIsAuthenticated] = useState(false); // Using a separate flag or derived from token? Derived is safer but for now sync state.
    const router = useRouter();

    useEffect(() => {
        // Init from localStorage
        const storedToken = localStorage.getItem('token');
        if (storedToken) {
            setToken(storedToken);
            setIsAuthenticated(true);
        }
    }, []);

    const login = (newToken: string) => {
        localStorage.setItem('token', newToken);
        document.cookie = `token=${newToken}; path=/; max-age=18000; SameSite=Lax`;
        setToken(newToken);
        setIsAuthenticated(true);
        router.push('/admin'); // Redirect to admin after login
    };

    const logout = () => {
        localStorage.removeItem('token');
        document.cookie = "token=; path=/; max-age=0";
        setToken(null);
        setIsAuthenticated(false);
        router.push('/login');
    };

    return (
        <AuthContext.Provider value={{ token, login, logout, isAuthenticated }}>
            {children}
        </AuthContext.Provider>
    );
};

export const useAuth = () => useContext(AuthContext);
