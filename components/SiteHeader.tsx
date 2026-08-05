"use client";

import Link from "next/link";
import { useEffect, useState } from "react";
import { AuthControls } from "@/components/AuthControls";
import { fetchEntitlement } from "@/lib/payment";

export function SiteHeader() {
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
          <h1>Math Worksheet Generator</h1>
          <p>Create printable practice worksheets for your students.</p>
          <nav className="site-nav" aria-label="Primary">
            <Link href="/">Generator</Link>
            <Link href="/gallery">Example gallery</Link>
          </nav>
        </div>
        <AuthControls
          entitled={entitled}
          authConfigured={authConfigured}
          onError={setError}
        />
      </div>
      {error && <p className="error">{error}</p>}
    </header>
  );
}
