import type { Metadata } from "next";
import "katex/dist/katex.min.css";
import "./globals.css";
import { AuthProvider } from "@/components/AuthProvider";
import { SiteHeader } from "@/components/SiteHeader";
import { DifficultyKnobsDebug } from "@/components/DifficultyKnobsDebug";

export const metadata: Metadata = {
  title: "Math Worksheet Generator",
  description: "Generate printable math worksheets with randomized questions.",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>
        <AuthProvider>
          <main className="container">
            <SiteHeader />
            {children}
          </main>
          <DifficultyKnobsDebug />
        </AuthProvider>
      </body>
    </html>
  );
}
