"use client"

import { useState } from 'react';

// Wait, Card is in '@/components/ui/card'.
import { Card as ShadcnCard, CardContent as ShadcnCardContent, CardHeader as ShadcnCardHeader } from '@/components/ui/card';
import { Button } from '@/components/ui/button';

interface Translation {
    language: string;
    translated_content: string;
}

interface Post {
    id: number;
    image_path: string | null;
    created_at: string;
    original_text: string;
    translations: Translation[];
}

const LANGUAGES = [
    { code: 'en', label: 'English', flag: '🇺🇸' },
    { code: 'zh-tw', label: '繁體中文', flag: '🇹🇼' },
    { code: 'zh-cn', label: '简体中文', flag: '🇨🇳' },
    { code: 'ko', label: '한국어', flag: '🇰🇷' },
    { code: 'ja', label: '日本語', flag: '🇯🇵' },
];

export default function PostCard({ post }: { post: Post }) {
    const [currentLang, setCurrentLang] = useState('en');

    // Find content for the selected language
    // If not found (e.g. Japanese might be in original_text or translations['ja']), handling fallback
    const getContent = (lang: string) => {
        const translation = post.translations.find(t => t.language === lang);
        if (translation) return translation.translated_content;

        // Fallbacks
        if (lang === 'ja') return post.original_text; // Assuming original is JA
        return post.original_text;
    };

    return (
        <ShadcnCard className="overflow-hidden border-none shadow-md hover:shadow-lg transition-shadow flex flex-col">
            <div className="aspect-video relative bg-gray-200">
                {post.image_path ? (
                    <img
                        src={`http://localhost:8000${post.image_path}`}
                        alt="Post"
                        className="object-cover w-full h-full"
                    />
                ) : (
                    <div className="flex items-center justify-center h-full text-gray-400">No Image</div>
                )}
                {/* Overlay Language Switcher? Or below? User said "Horizontal buttons or slide". Below image is safer. */}
            </div>

            <ShadcnCardHeader className="p-4 pb-2">
                {/* Scrollable Language Selector */}
                <div className="flex gap-2 overflow-x-auto pb-2 scrollbar-hide">
                    {LANGUAGES.map((lang) => (
                        <Button
                            key={lang.code}
                            variant={currentLang === lang.code ? "default" : "outline"}
                            size="sm"
                            className="rounded-full px-3 py-1 h-8 text-xs whitespace-nowrap"
                            onClick={() => setCurrentLang(lang.code)}
                        >
                            {lang.flag} {lang.label}
                        </Button>
                    ))}
                </div>
                <div className="flex justify-between items-center mt-2">
                    <span className="text-xs text-gray-400">
                        {new Date(post.created_at).toLocaleDateString()}
                    </span>
                </div>
            </ShadcnCardHeader>

            <ShadcnCardContent className="p-4 pt-0">
                <div className="text-sm text-gray-800 min-h-[4rem] whitespace-pre-wrap">
                    {getContent(currentLang)}
                </div>
            </ShadcnCardContent>
        </ShadcnCard>
    );
}
