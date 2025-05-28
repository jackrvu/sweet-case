import Link from 'next/link';
import Layout from '@/components/layout';

export default function Specs() {
  // Define sidebar content
  const sidebarContent = (
    <>
      <div className="border border-black p-2">
        <h2 className="font-semibold">Navigation</h2>
      </div>
      <div className="mb-4 border border-black border-t-0 p-2">
        <ul className="space-y-1">
          <li><Link href="/" className="hover:text-indigo-500 transition-colors duration-200">Home</Link></li>
          <li><Link href="/posts" className="hover:text-indigo-500 transition-colors duration-200">All Posts</Link></li>
        </ul>
      </div>
    </>
  );

  // Main content
  const mainContent = (
    <>
      <div className="border border-black p-2">
        <h2 className="font-semibold">Digital Doorways</h2>
      </div>
      <div className="mb-4 border border-black border-t-0 p-2">
        <p className="italic mb-4 text-gray-600">news coverage & information</p>
        
        <div className="space-y-3">
          <p>
            <a 
              href="https://thebuzzmagazines.com/articles/2024/08/digital-doorways" 
              target="_blank" 
              rel="noopener noreferrer" 
              className="text-indigo-500 hover:underline"
            >
              West University Buzz Article
            </a>
            <br />
            <a 
              href="https://www.digitaldoorways.org/" 
              target="_blank" 
              rel="noopener noreferrer" 
              className="text-indigo-500 hover:underline"
            >
              Organization Website
            </a>
            <br />
            <a 
              href="https://www.instagram.com/dig_doorways/" 
              target="_blank" 
              rel="noopener noreferrer" 
              className="text-indigo-500 hover:underline"
            >
              Instagram
            </a>
          </p>
        </div>
      </div>
    </>
  );

  return (
    <Layout sidebarContent={sidebarContent}>
      {mainContent}
    </Layout>
  );
}