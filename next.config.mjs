/** @type {import('next').NextConfig} */
const nextConfig = {
  async rewrites() {
    // Local Next (dev or `next start`) proxies to the Python question engine.
    // On Vercel, generation is handled by the platform separately.
    if (process.env.VERCEL) {
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
