import Pokemon from '@/components/pokemon';
import PostsList from '@/components/postslist';
import ProjectsList from '@/components/projects';
import Layout from '@/components/layout';
import { getRecentLinks } from '@/data/links';  
import {getRecentPosts} from '@/data/posts';
import LinksList from '@/components/postlinkslist';
export default function HomePage() {
  // Define sidebar content
  const sidebarContent = (
    <>
      <div className="border border-black p-2 w-[100%]">
      <h2 className="font-semibold">About me</h2>
      </div>
      <div className="mb-4 border border-black border-t-0 p-2 w-[100%]">
      <p className="tracking-very-tight">rice cs & math '29</p>
      </div>

      <div className="border border-black p-2 w-[100%]">
      <h2 className="font-semibold">Status</h2>
      </div>
      <div className="mb-4 border border-black border-t-0 p-2 flex items-center gap-2 w-[100%]">
      signal chasing
      </div>
      
      <div className="border border-black p-2 w-[100%]">
      <h2 className="font-semibold">Contacts</h2>
      </div>
      <div className="mb-4 border border-black border-t-0 p-2 w-[100%]">
      <ul className="space-y-1">
        <li><a href="https://github.com/jackrvu" className="hover:text-fuchsia-400 transition-colors duration-200">github.com/jackrvu</a></li>
        <li><a href="mailto:jvu@rice.edu" className="hover:text-indigo-400 transition-colors duration-200">jvu@rice.edu</a></li>
      </ul>
      </div>

      <div className="border border-black p-2 w-[100%]">
        <h2 className="font-semibold">Press</h2>
      </div>
      <LinksList postlinks={getRecentLinks()} />
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
      <div className="text-xs text-gray-500 mt-4 flex justify-center items-center text-center">
        <p>website design from my friend&nbsp;</p>
        <a href="https://enbao.me" className="text-blue-500 visited:text-purple-500 hover:underline">enbao</a>
      </div>
    </Layout>
  );
}
