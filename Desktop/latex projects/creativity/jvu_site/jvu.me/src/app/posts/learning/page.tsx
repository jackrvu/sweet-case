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
        <h2 className="font-semibold">Learning</h2>
      </div>
      <div className="mb-4 border border-black border-t-0 p-2">
        <p className="italic mb-4 text-gray-600">some paragraphs I scribbled down in august of '24.</p>
        
        <div className="space-y-4 leading-relaxed">
          <p>Have you seen the world? Have you seen the incredible things you can do with just a computer, words, and turning shapes over in your mind? Have you seen how you can provide a service to others, something they didn't even know they wanted, and push a noticeable change into the world?</p>
          
          <p>The worst thing, the ultimate blocker to learning, is something, some course, some person, who explains things to you as if you don't have the capability to understand it yourself. Every person here should be imbued with the innate knowledge that they have the ability to learn and understand anything and everything. If you put the time in. If you devote yourself to it. If you ask the textbook questions and hunt for the answers. If you use the internet to help you on your search. If you find yourself thinking about the problem in the shower.</p>
          
          <p>The best motivator of learning is other people. Thankfully, the internet made finding a group of like-minded people that are excited to learn and build easier than ever. Find your community and grow alongside. When you step back and take a look at others around you, you'll be surprised by how much you've changed and grown.</p>
          
          <p>If you ever feel insecure about the value of your life, try learning something you care deeply about.</p>
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