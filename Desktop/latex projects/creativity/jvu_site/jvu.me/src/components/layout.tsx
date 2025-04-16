import React, { ReactNode } from 'react';
import Header from './header';

interface LayoutProps {
  children: ReactNode;
  sidebarContent: ReactNode;
}

export default function Layout({ children, sidebarContent }: LayoutProps) {
  return (
    <div className="no-select flex flex-col w-full h-full px-4 md:px-6 lg:px-8 max-w-6xl mx-auto">
      <Header />
      <div className="flex flex-col md:flex-row flex-grow text-3xs lg:text-2xs gap-4">
        <aside className="w-full md:w-1/3 h-full mb-4 md:mb-0 md:mr-4">
          {sidebarContent}
        </aside>
        <main className="w-full md:w-2/3 h-full">
          {children}
        </main>
      </div>
    </div>
  );
}