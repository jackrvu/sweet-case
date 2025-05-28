import Link from 'next/link';

export default function Header() {
  return (
    <header className="py-6 mb-6 border-b border-black">
      <div className="flex flex-col md:flex-row md:items-end md:justify-between">
        <div>
          <h1 className="text-xl lg:text-2xl font-bold">Jack Vu</h1>
          <p className="text-xs lg:text-sm text-gray-700">tuned in.</p>
        </div>
        <nav className="mt-2 md:mt-0">
          <ul className="flex space-x-4 text-sm">
            <li><Link href="/" className="hover:text-indigo-500 transition-colors duration-200">home</Link></li>
            <li><Link href="/posts" className="hover:text-indigo-500 transition-colors duration-200">posts</Link></li>
          </ul>
        </nav>
      </div>
    </header>
  );
}