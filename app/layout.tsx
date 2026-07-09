import type { Metadata } from "next";
import "katex/dist/katex.min.css";
import "./globals.css";
import { WorksheetGenerator } from "@/components/WorksheetGenerator";

export const metadata: Metadata = {
  title: "Math Worksheet Generator",
  description: "Generate printable math worksheets with randomized questions.",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>
        <main className="container">
          <header className="site-header">
            <h1>Math Worksheet Generator</h1>
            <p>Create printable practice worksheets for your students.</p>
          </header>
          {children}
        </main>
      </body>
    </html>
  );
}
