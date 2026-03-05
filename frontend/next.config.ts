import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  // export the site as a fully static application so that `next build`
  // produces an `out/` directory we can serve from FastAPI.
  output: 'export',
};

export default nextConfig;
