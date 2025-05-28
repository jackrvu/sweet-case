import Link from 'next/link';
import Layout from '@/components/layout';
import fs from 'fs';
import path from 'path';

// Recursively gather all image paths from a directory
function getAllImages(dir: string): string[] {
    let results: string[] = [];
    const list = fs.readdirSync(dir);
    list.forEach((file) => {
        const filePath = path.join(dir, file);
        const stat = fs.statSync(filePath);
        if (stat.isDirectory()) {
            results = results.concat(getAllImages(filePath));
        } else if (/\.(jpe?g|png|gif|svg|webp)$/i.test(file)) {
            // Convert absolute path to a relative path for Next to use
            const relative = filePath
                .replace(path.join(process.cwd(), 'public'), '')
                .replace(/\\/g, '/');
            results.push(relative);
        }
    });
    return results;
}

export default function Specs() {
    const imagesDir = path.join(process.cwd(), 'public', 'assets', 'plots');
    const allImages = getAllImages(imagesDir);

    const sidebarContent = (
        <>
            <div className="border border-black p-2">
                <h2 className="font-semibold">Navigation</h2>
            </div>
            <div className="mb-4 border border-black border-t-0 p-2">
                <ul className="space-y-1">
                    <li>
                        <Link href="/" className="hover:text-indigo-500 transition-colors duration-200">
                            Home
                        </Link>
                    </li>
                    <li>
                        <Link href="/posts" className="hover:text-indigo-500 transition-colors duration-200">
                            All Posts
                        </Link>
                    </li>
                </ul>
            </div>
        </>
    );

    const mainContent = (
        <>
            <div className="border border-black p-2">
                <h2 className="font-semibold">Findings & Reflections</h2>
            </div>
            <div className="mb-4 border border-black border-t-0 p-2">
                <p className="mb-4 text-gray-600">Jewel's notably high entropy aligns with his intense, emotionally charged, and unpredictable narrative style. His lexical variability echoes his complex inner turmoil and defiance.

Whitfield’s elevated entropy similarly fits with his distinctive narrative voice. Typically interpreted as morally conflicted and self-justifying, Whitfield’s high lexical entropy may signify his internal psychological contradictions, manifesting in linguistically diverse expressions.

Conversely, the low entropy ratios observed in narrators like Darl and Tull strongly correlate with our classroom observations, as well as those from referenced scholarly articles. Darl, known for his introspective, obsessive, and repetitive cognitive style, predictably exhibits a constrained lexical profile, underscoring his thematic role as a figure haunted by fixation and mental fragmentation. Similarly, Tull’s simpler and more direct narrative approach, characteristic of his pragmatic worldview, is mirrored in his lower entropy score.

In essence, these entropy calculations quantitatively reinforce conventional literary analyses.</p>
                <div className="space-y-3">
                    {allImages.map((src, idx) => (
                        <div key={idx} className="flex justify-center my-4">
                            <img src={src} alt={`Plot ${idx + 1}`} className="max-w-full h-auto border" />
                        </div>
                    ))}
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