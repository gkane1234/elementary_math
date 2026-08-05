"use client";

import { signIn } from "next-auth/react";
import Link from "next/link";

export default function SignInPage() {
  return (
    <section className="panel payment-status">
      <h2>Sign in</h2>
      <p>Sign in with Google to subscribe for unlimited worksheets, or manage an existing Pro plan.</p>
      <div className="payment-actions">
        <button className="primary" type="button" onClick={() => signIn("google", { callbackUrl: "/" })}>
          Continue with Google
        </button>
        <Link className="secondary button-link" href="/">
          Back to worksheet
        </Link>
      </div>
    </section>
  );
}
