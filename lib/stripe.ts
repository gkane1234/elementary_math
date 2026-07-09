import Stripe from "stripe";

let stripeClient: Stripe | null = null;

const VALID_SECRET_KEY_PREFIXES = ["sk_test_", "sk_live_", "rk_test_", "rk_live_"];

export function isValidStripeSecretKey(key: string | undefined): key is string {
  if (!key) {
    return false;
  }

  return VALID_SECRET_KEY_PREFIXES.some((prefix) => key.startsWith(prefix));
}

export function stripeKeyError(key: string | undefined): string | null {
  if (!key) {
    return "STRIPE_SECRET_KEY is not configured.";
  }

  if (key.startsWith("mk_")) {
    return "STRIPE_SECRET_KEY is a merchant key (mk_). Use a secret key (sk_test_...) from the Stripe Dashboard instead.";
  }

  if (key.startsWith("pk_")) {
    return "STRIPE_SECRET_KEY is a publishable key (pk_). Use a secret key (sk_test_...) from the Stripe Dashboard instead.";
  }

  if (!isValidStripeSecretKey(key)) {
    return "STRIPE_SECRET_KEY must start with sk_test_, sk_live_, rk_test_, or rk_live_.";
  }

  return null;
}

export function isStripeConfigured(): boolean {
  return isValidStripeSecretKey(process.env.STRIPE_SECRET_KEY);
}

export function getStripe(): Stripe {
  const secretKey = process.env.STRIPE_SECRET_KEY;
  const keyError = stripeKeyError(secretKey);
  if (keyError || !isValidStripeSecretKey(secretKey)) {
    throw new Error(keyError ?? "STRIPE_SECRET_KEY is not configured.");
  }

  if (!stripeClient) {
    stripeClient = new Stripe(secretKey);
  }

  return stripeClient;
}

export function getPdfPriceCents(): number {
  const raw = process.env.STRIPE_PDF_PRICE_CENTS;
  const parsed = raw ? Number.parseInt(raw, 10) : 300;
  return Number.isFinite(parsed) && parsed > 0 ? parsed : 300;
}

export function getAppOrigin(request: Request): string {
  const configured = process.env.NEXT_PUBLIC_APP_URL;
  if (configured) {
    return configured.replace(/\/$/, "");
  }

  const host = request.headers.get("x-forwarded-host") ?? request.headers.get("host");
  const proto = request.headers.get("x-forwarded-proto") ?? "http";
  if (host) {
    return `${proto}://${host}`;
  }

  return "http://localhost:3000";
}
