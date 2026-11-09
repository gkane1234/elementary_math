"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { useEffect, useState } from "react";
import { AuthControls } from "@/components/AuthControls";
import { GENERATOR_PATH } from "@/lib/landing";
import { fetchEntitlement } from "@/lib/payment";

export function SiteHeader() {
  const pathname = usePathname();
  const onGenerate = pathname === GENERATOR_PATH;
  const onGallery = pathname.startsWith("/gallery");
  const [entitled, setEntitled] = useState(false);
  const [authConfigured, setAuthConfigured] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    fetchEntitlement()
      .then((data) => {
        setAuthConfigured(data.authConfigured);
        setEntitled(data.entitled && data.reason !== "payments_disabled" && Boolean(data.status));
      })
      .catch(() => {
        setEntitled(false);
      });
  }, []);

  return (
    <header className="site-header">
      <div className="site-header-row">
        <div>
          <p className="site-wordmark">
            <Link href="/">Math Worksheet Generator</Link>
          </p>
          <nav className="site-nav" aria-label="Primary">
            <Link href={GENERATOR_PATH} aria-current={onGenerate ? "page" : undefined}>
              Generator
            </Link>
            <Link href="/gallery" aria-current={onGallery ? "page" : undefined}>
              Examples
            </Link>
          </nav>
        </div>
        <div className="site-header-actions">
          {onGenerate ? null : (
            <Link className="header-cta" href={GENERATOR_PATH}>
              Open the generator
            </Link>
          )}
          <AuthControls
            entitled={entitled}
            authConfigured={authConfigured}
            onError={setError}
          />
        </div>
      </div>
      {error && <p className="error">{error}</p>}
    </header>
  );
}
