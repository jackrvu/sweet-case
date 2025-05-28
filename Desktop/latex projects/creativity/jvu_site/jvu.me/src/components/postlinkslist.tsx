// src/components/PostsList.tsx
import Link from 'next/link';

type postlink = {
  title: string;
  slug: string;
};

type PostsListProps = {
  postlinks: readonly postlink[] | postlink[];
};

export default function LinksList({ postlinks }: PostsListProps) {
  return (
    <div className="mb-4 border border-black border-t-0 p-2 w-[100%]">
      {postlinks.length > 0 ? (
        <ul className="space-y-1">
          {postlinks.map((postlink) => (
            <li key={postlink.slug} className="-mx-1 px-1 py-0.5 rounded">
              <Link href={`/links/${postlink.slug}`} className="flex flex-row items-baseline group">
                <span className="group-hover:text-green-500 transition-colors duration-200">{postlink.title}</span>
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