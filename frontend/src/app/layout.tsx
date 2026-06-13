import { TooltipProvider } from '@/components/ui/tooltip';
import type { Metadata } from 'next';
import { Inter, JetBrains_Mono } from 'next/font/google';
import Header from '@/components/layout/Header';
import Footer from '@/components/layout/Footer';
import './globals.css';

const inter = Inter({
  subsets: ['latin'],
  variable: '--font-sans',
});

const jetbrainsMono = JetBrains_Mono({
  subsets: ['latin'],
  variable: '--font-mono',
});

export const metadata: Metadata = {
  title: 'TypeForge | Premium Typing Platform',
  description: 'Ultra-fast, AI-enhanced typing platform with multiplayer racing and analytics.',
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" suppressHydrationWarning>
      <body
        className={`${inter.variable} ${jetbrainsMono.variable} font-sans antialiased min-h-screen flex flex-col`}
      >
        <TooltipProvider delay={150}>
          <div className="max-w-[1250px] mx-auto w-full px-4 sm:px-6 lg:px-8 flex flex-col flex-1">
            <Header />
            <main className="flex-1 flex flex-col pt-12 pb-24">
              {children}
            </main>
            <Footer />
          </div>
        </TooltipProvider>
      </body>
    </html>
  );
}
