// src/data/posts.ts
export const links = [
    { title: 'Digital Doorways', slug: 'digital_doorways' },
    { title: 'M3 Contest', slug: 'm3' },
    { title: 'Mav Hub', slug: 'mavhub' },
    // { date: '25-00-00', title: 'three', slug: 'intro' } // Removed
] as const;

// if u need just recent posts somewhere
export const getRecentLinks = () => links.slice(0, 10);