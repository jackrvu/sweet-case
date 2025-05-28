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
        <h2 className="font-semibold">Mathworks Math Modeling Contest</h2>
      </div>
      <div className="mb-4 border border-black border-t-0 p-2">
        <p className="italic mb-4 text-gray-600">news coverage</p>
        
        <div className="space-y-3">
          <p>
            <a 
              href="https://www.click2houston.com/features/2025/04/07/houston-students-advance-to-finals-in-prestigious-international-math-competition/" 
              target="_blank" 
              rel="noopener noreferrer" 
              className="text-indigo-500 hover:underline"
            >
              KPRC2 Article
            </a>
            <br />
            <a 
              href="https://www.fox26houston.com/news/houston-area-high-school-students-could-possibly-win-100k-after-advancing-finals-math-competition" 
              target="_blank" 
              rel="noopener noreferrer" 
              className="text-indigo-500 hover:underline"
            >
              FOX26 Article
            </a>
            <br />
            <a 
              href="https://www.youtube.com/watch?v=vB1t8jKqRok/" 
              target="_blank" 
              rel="noopener noreferrer" 
              className="text-indigo-500 hover:underline"
            >
              FOX26 Video
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