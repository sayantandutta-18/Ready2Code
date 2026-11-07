/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: false,
  output: "standalone",
  webpack: (config) => {
    config.externals = [...(config.externals || []), { canvas: "canvas" }];
    return config;
  },
  async rewrites() {
    const rawTarget = process.env.API_INTERNAL_URL || process.env.NEXT_PUBLIC_API_URL || 'https://api-production-4000.up.railway.app';
    const targetBase = rawTarget.replace(/\/$/, '');
    return [
      {
        source: '/api/:path*',
        destination: `${targetBase}/:path*`,
      },
    ];
  },
};

module.exports = nextConfig;
