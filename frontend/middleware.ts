import { NextResponse } from 'next/server'
import type { NextRequest } from 'next/server'
 
export function middleware(request: NextRequest) {
  // 管理画面 (/admin) 配下のパスへのアクセスかチェック
  if (request.nextUrl.pathname.startsWith('/admin')) {
    
    // Cookie からトークンを取得
    const token = request.cookies.get('token')
 
    // トークンがない場合はログイン画面へ強制リダイレクト
    if (!token) {
      return NextResponse.redirect(new URL('/login', request.url))
    }
  }
  
  // 問題なければそのまま通す
  return NextResponse.next()
}
 
// 適用するパスの設定
export const config = {
  matcher: '/admin/:path*',
}