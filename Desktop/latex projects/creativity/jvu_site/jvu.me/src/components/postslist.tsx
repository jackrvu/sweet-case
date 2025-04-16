// src/components/PostsList.tsx
import Link from 'next/link';

type Post = {
  date: string;
  title: string;
  slug: string;
};

type PostsListProps = {
  posts: readonly Post[] | Post[];
};

export default function PostsList({ posts }: PostsListProps) {
  return (
    <div className="mb-4 border border-black border-t-0 p-2">
      {posts.length > 0 ? (
        <ul className="space-y-1">
          {posts.map((post) => (
            <li key={post.slug} className="-mx-1 px-1 py-0.5 rounded">
              <Link href={`/posts/${post.slug}`} className="flex flex-row items-baseline group">
                <span className="text-gray-600 mr-3 text-xs">{post.date}</span>
                <span className="group-hover:text-green-500 transition-colors duration-200">{post.title}</span>
              </Link>
            </li>
          ))}
        </ul>
      ) : (
        <p className="text-gray-500 italic">No posts available</p>
      )}
    </div>
  );
}