import type { NextConfig } from "next";
import path from "path";

const nextConfig: NextConfig = {
  // 避免上層目錄另有 package-lock 時，Turbopack 誤判 workspace root
  turbopack: {
    root: path.join(__dirname),
  },
};

export default nextConfig;
