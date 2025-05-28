// src/data/posts.ts
export const posts = [
    { date: '04-03-25', title: 'the stack', slug: 'intro' }
    // { date: '25-00-00', title: 'three', slug: 'intro' } // Removed
] as const;

// if u need just recent posts somewhere
export const getRecentPosts = () => posts.slice(0, 3);