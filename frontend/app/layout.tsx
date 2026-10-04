import type { Metadata } from "next";
import "./globals.css";
import Link from "next/link";
import 'leaflet/dist/leaflet.css';

export const metadata: Metadata = {
  title: "EcoSmart Bins",
  description: "Monitoring irregular garbage collection using data analytics, GIS and machine learning.",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body className="font-sans antialiased">
        <nav className="bg-white shadow-sm border-b sticky top-0 z-50">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="flex justify-between h-16">
              <div className="flex items-center gap-6">
                <Link href="/" className="flex-shrink-0 flex items-center font-bold text-xl text-blue-600">
                  EcoSmart Bins
                </Link>
                <div className="flex space-x-4">
                  <Link href="/" className="text-slate-700 hover:text-blue-600 px-3 py-2 rounded-md text-sm font-medium transition-colors">Resident</Link>
                  <Link href="/admin" className="text-slate-700 hover:text-blue-600 px-3 py-2 rounded-md text-sm font-medium transition-colors">Admin Dashboard</Link>
                </div>
              </div>
            </div>
          </div>
        </nav>
        <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          {children}
        </main>
      </body>
    </html>
  );
}
