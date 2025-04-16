import Link from 'next/link';
import Layout from '@/components/layout';

export default function WebsiteUpdate() {
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
        <h2 className="font-semibold">Website Update</h2>
      </div>
      <div className="mb-4 border border-black border-t-0 p-2">
        <p className="italic mb-4 text-gray-600">changes and improvements to the site.</p>
        
        <div className="space-y-4 leading-relaxed">
          <p>I've made several improvements to my personal website today:</p>
          
          <ul className="list-disc pl-5 space-y-2">
            <li>Enhanced the styling and layout for better responsiveness</li>
            <li>Created a consistent design system across all pages</li>
            <li>Fixed alignment issues between post dates and titles</li>
            <li>Made project titles bold with gray descriptions for better readability</li>
            <li>Removed unused code and simplified the codebase</li>
          </ul>
          
          <p>The site now has a cleaner, more consistent look while maintaining its minimalist aesthetic. I'll continue to iterate on the design as I add more content.</p>
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