import type { NextConfig } from "next";

// When BUILD_EXPORT=1 (set in Dockerfile), produce a static out/ directory.
// In dev mode (next dev), rewrites proxy /api/* to the FastAPI backend.
const isStaticExport = process.env.BUILD_EXPORT === "1";

const nextConfig: NextConfig = {
  output: isStaticExport ? "export" : undefined,
  ...(!isStaticExport && {
    async rewrites() {
      return [
        {
          source: "/api/:path*",
          destination: "http://localhost:8000/api/:path*",
        },
      ];
    },
  }),
};

export default nextConfig;
