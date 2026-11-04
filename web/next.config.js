/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: false,
  output: "standalone",
  webpack: (config) => {
    config.externals = [...(config.externals || []), { canvas: "canvas" }];
    return config;
  },
  async rewrites() {
    const apiTarget = process.env.API_INTERNAL_URL || 'http://localhost:8000/:path*';
    return [
      {
        source: '/api/:path*',
        destination: apiTarget,
      },
    ]
  },
}

module.exports = nextConfig
