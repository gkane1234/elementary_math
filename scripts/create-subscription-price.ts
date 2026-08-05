/**
 * Creates a $10/mo Stripe Price for Polynomial Pro and prints the price id.
 * Usage: npx --yes tsx scripts/create-subscription-price.ts
 *
 * Requires STRIPE_SECRET_KEY in .env.local (or the environment).
 */
import { readFileSync, writeFileSync, existsSync } from "fs";
import path from "path";
import Stripe from "stripe";

const root = path.join(__dirname, "..");
const envPath = path.join(root, ".env.local");

function readEnvValue(name: string): string | null {
  if (!existsSync(envPath)) {
    return null;
  }
  for (const line of readFileSync(envPath, "utf-8").split(/\r?\n/)) {
    const match = line.match(new RegExp(`^${name}=(.*)$`));
    if (match) {
      const value = match[1].trim();
      return value || null;
    }
  }
  return null;
}

function upsertEnvLine(key: string, value: string) {
  const raw = existsSync(envPath) ? readFileSync(envPath, "utf-8") : "";
  const lines = raw.length ? raw.split(/\r?\n/) : [];
  let found = false;
  const next = lines.map((line) => {
    if (line.match(new RegExp(`^${key}=`))) {
      found = true;
      return `${key}=${value}`;
    }
    return line;
  });
  if (!found) {
    if (next.length && next[next.length - 1] !== "") {
      next.push("");
    }
    next.push(`${key}=${value}`);
  }
  writeFileSync(envPath, `${next.filter((line, index, arr) => !(index === arr.length - 1 && line === "")).join("\n")}\n`, "utf-8");
}

async function main() {
  const secret = process.env.STRIPE_SECRET_KEY || readEnvValue("STRIPE_SECRET_KEY");
  if (!secret || !/^(sk_|rk_)(test_|live_)/.test(secret)) {
    throw new Error("Set STRIPE_SECRET_KEY in .env.local first (npm run setup:stripe).");
  }

  const existing = readEnvValue("STRIPE_SUBSCRIPTION_PRICE_ID");
  if (existing?.startsWith("price_")) {
    console.log(`Already configured: ${existing}`);
    return;
  }

  const stripe = new Stripe(secret);
  const product = await stripe.products.create({
    name: "Polynomial Pro",
    description: "Unlimited worksheet answer keys and PDF exports",
  });

  const price = await stripe.prices.create({
    product: product.id,
    currency: "usd",
    unit_amount: 1000,
    recurring: { interval: "month" },
  });

  upsertEnvLine("STRIPE_SUBSCRIPTION_PRICE_ID", price.id);
  upsertEnvLine("STRIPE_SUBSCRIPTION_PRICE_CENTS", "1000");

  console.log(`Created product ${product.id}`);
  console.log(`Created price ${price.id} ($10/mo)`);
  console.log(`Wrote STRIPE_SUBSCRIPTION_PRICE_ID to .env.local`);
}

main().catch((error) => {
  console.error(error instanceof Error ? error.message : error);
  process.exit(1);
});
