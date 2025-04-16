/** @type {import('next').NextConfig} */
const nextConfig = {
  output: 'export',
  images: {
    unoptimized: true,
  },
  // Don't specify assetPrefix to avoid font issues
}

module.exports = nextConfig