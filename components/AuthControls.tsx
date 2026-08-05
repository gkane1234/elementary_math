"use client";

import { signIn, signOut, useSession } from "next-auth/react";
import { useState } from "react";
import { openBillingPortal } from "@/lib/payment";

type AuthControlsProps = {
  entitled?: boolean;
  authConfigured?: boolean;
  onError?: (message: string) => void;
};

export function AuthControls({
  entitled = false,
  authConfigured = true,
  onError,
}: AuthControlsProps) {
  const { data: session, status } = useSession();
  const [portalLoading, setPortalLoading] = useState(false);

  if (!authConfigured) {
    return (
      <div className="auth-controls">
        <span className="auth-hint">Auth not configured</span>
      </div>
    );
  }

  if (status === "loading") {
    return (
      <div className="auth-controls">
        <span className="auth-hint">Checking sign-in…</span>
      </div>
    );
  }

  if (!session?.user) {
    return (
      <div className="auth-controls">
        <button className="secondary" type="button" onClick={() => signIn("google")}>
          Sign in with Google
        </button>
      </div>
    );
  }

  const handlePortal = async () => {
    setPortalLoading(true);
    onError?.("");
    try {
      const url = await openBillingPortal();
      window.location.assign(url);
    } catch (error) {
      const message = error instanceof Error ? error.message : "Could not open billing portal";
      onError?.(message);
      setPortalLoading(false);
    }
  };

  return (
    <div className="auth-controls">
      <div className="auth-user">
        {session.user.image ? (
          // eslint-disable-next-line @next/next/no-img-element
          <img className="auth-avatar" src={session.user.image} alt="" width={28} height={28} />
        ) : null}
        <span className="auth-name">{session.user.name ?? session.user.email}</span>
        {entitled && <span className="auth-badge">Pro</span>}
      </div>
      {entitled && (
        <button className="secondary" type="button" onClick={handlePortal} disabled={portalLoading}>
          {portalLoading ? "Opening…" : "Manage billing"}
        </button>
      )}
      <button className="secondary" type="button" onClick={() => signOut()}>
        Sign out
      </button>
    </div>
  );
}
