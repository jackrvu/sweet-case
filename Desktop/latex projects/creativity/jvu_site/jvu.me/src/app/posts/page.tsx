import Link from 'next/link';
import PostsList from '@/components/postslist';
import Layout from '@/components/layout';
import { posts } from '@/data/posts';

export default function PostsPage() {
  // Define sidebar content
  const sidebarContent = (
    <>
      <div className="border border-black p-2">
        <h2 className="font-semibold">Navigation</h2>
      </div>
      <div className="mb-4 border border-black border-t-0 p-2">
        <ul className="space-y-1">
          <li><Link href="/" className="hover:text-indigo-500 transition-colors duration-200">Back to Home</Link></li>
        </ul>
      </div>
      
      <div className="border border-black p-2">
        <h2 className="font-semibold">Archives</h2>
      </div>
      <div className="mb-4 border border-black border-t-0 p-2">
        <p className="text-gray-600">Post archives coming soon...</p>
      </div>
    </>
  );

  // Main content
  const mainContent = (
    <>
      <div className="border border-black p-2">
        <h2 className="font-semibold">All Posts</h2>
      </div>
      <PostsList posts={posts} />
    </>
  );

  return (
    <Layout sidebarContent={sidebarContent}>
      {mainContent}
    </Layout>
  );
}