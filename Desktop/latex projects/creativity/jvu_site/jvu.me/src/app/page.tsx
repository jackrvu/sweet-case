import Pokemon from '@/components/pokemon';
import PostsList from '@/components/postslist';
import ProjectsList from '@/components/projects';
import Layout from '@/components/layout';
import { getRecentPosts } from '@/data/posts';

export default function HomePage() {
  // Define sidebar content
  const sidebarContent = (
    <>
      <div className="border border-black p-2 w-[115%]">
        <h2 className="font-semibold">About me</h2>
      </div>
      <div className="mb-4 border border-black border-t-0 p-2 w-[115%]">
        <p className="tracking-very-tight">rice cs & math '29</p>
      </div>

      <div className="border border-black p-2 w-[115%]">
        <h2 className="font-semibold">Status</h2>
      </div>
      <div className="mb-4 border border-black border-t-0 p-2 flex items-center gap-2 w-[115%]">
        changing my mind
      </div>
      
      <div className="border border-black p-2 w-[115%]">
        <h2 className="font-semibold">Links</h2>
      </div>
      <div className="mb-4 border border-black border-t-0 p-2 w-[115%]">
        <ul className="space-y-1">
          <li><a href="https://github.com/jackrvu" className="hover:text-fuchsia-400 transition-colors duration-200">github.com/jackrvu</a></li>
          <li><a href="mailto:jackrvu@gmail.com" className="hover:text-indigo-400 transition-colors duration-200">jackrvu[at]gmail[dot]com</a></li>
        </ul>
      </div>
    </>
  );

  // Main content
  const mainContent = (
    <>
      <div className="border border-black p-2">
        <h2 className="font-semibold">Blog</h2>
      </div>
      <PostsList posts={getRecentPosts()} />  
      <div className="border border-black p-2">
        <h2 className="font-semibold">Projects</h2>
      </div>
      <div className="mb-4 border border-black border-t-0 p-2">
        <ProjectsList />
      </div>
    </>
  );

  return (
    <Layout sidebarContent={sidebarContent}>
      {mainContent}
    </Layout>
  );
}
