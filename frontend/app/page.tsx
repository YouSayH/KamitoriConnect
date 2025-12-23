"use client"

import { useEffect, useState } from 'react';
import Link from 'next/link';
import { Button } from '@/components/ui/button';
import PostCard from '@/components/PostCard'; // Import PostCard
import { MessageCircle } from 'lucide-react';
import api from '@/lib/api';

export default function Home() {
  const [posts, setPosts] = useState<any[]>([]);

  useEffect(() => {
    // Ideally we fetch posts here
    api.get('/posts').then(res => setPosts(res.data)).catch(err => console.error(err));
  }, []);

  return (
    <div className="container mx-auto px-4 py-8">
      <section className="mb-12 text-center">
        <h2 className="text-3xl font-extrabold text-gray-900 mb-4">Discover Kamitori</h2>
        <p className="text-gray-600 max-w-xl mx-auto">
          熊本の上通アーケード街で、隠れた名店や美味しいグルメ、文化的なスポットを見つけましょう。
        </p>
      </section>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {posts.map((post) => (
          <PostCard key={post.id} post={post} />
        ))}
      </div>


      {/* Floating Chat Button (Mobile) */}
      <div className="fixed bottom-6 right-6 md:hidden">
        <Link href="/chat">
          <Button size="icon" className="h-14 w-14 rounded-full shadow-xl">
            <MessageCircle size={24} />
          </Button>
        </Link>
      </div>
    </div >
  );
}
