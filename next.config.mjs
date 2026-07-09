/** @type {import('next').NextConfig} */
const nextConfig = {
  async rewrites() {
    if (process.env.NODE_ENV !== "development") {
      return [];
    }

    const apiBase = process.env.PYTHON_API_URL || "http://127.0.0.1:5328";
    return [
      { source: "/api/generate", destination: `${apiBase}/generate` },
      { source: "/api/question-types", destination: `${apiBase}/question-types` },
    ];
  },
};

export default nextConfig;
