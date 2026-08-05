import { promises as fs } from "fs";
import path from "path";

export type SubscriptionStatus =
  | "active"
  | "trialing"
  | "past_due"
  | "canceled"
  | "unpaid"
  | "incomplete"
  | "incomplete_expired"
  | "paused"
  | string;

export type StoredSubscription = {
  user_id: string;
  email: string | null;
  stripe_customer_id: string;
  stripe_subscription_id: string;
  status: SubscriptionStatus;
  current_period_end: string | null;
  updated_at: string;
};

const DATA_DIR = path.join(process.cwd(), ".data");
const DATA_FILE = path.join(DATA_DIR, "subscriptions.json");

declare global {
  // eslint-disable-next-line no-var
  var __subscriptionStore: Map<string, StoredSubscription> | undefined;
  // eslint-disable-next-line no-var
  var __subscriptionByCustomer: Map<string, string> | undefined;
}

function getMemoryStore(): Map<string, StoredSubscription> {
  if (!global.__subscriptionStore) {
    global.__subscriptionStore = new Map();
  }
  return global.__subscriptionStore;
}

function getCustomerIndex(): Map<string, string> {
  if (!global.__subscriptionByCustomer) {
    global.__subscriptionByCustomer = new Map();
  }
  return global.__subscriptionByCustomer;
}

function useFileStore(): boolean {
  return process.env.NODE_ENV === "development" || process.env.WORKSHEET_STORE_FILE === "true";
}

type FileStoreShape = {
  byUserId: Record<string, StoredSubscription>;
  byCustomerId: Record<string, string>;
};

async function readFileStore(): Promise<FileStoreShape> {
  try {
    const raw = await fs.readFile(DATA_FILE, "utf-8");
    const parsed = JSON.parse(raw) as FileStoreShape;
    return {
      byUserId: parsed.byUserId ?? {},
      byCustomerId: parsed.byCustomerId ?? {},
    };
  } catch {
    return { byUserId: {}, byCustomerId: {} };
  }
}

async function writeFileStore(data: FileStoreShape): Promise<void> {
  await fs.mkdir(DATA_DIR, { recursive: true });
  await fs.writeFile(DATA_FILE, JSON.stringify(data, null, 2), "utf-8");
}

export function isEntitled(status: SubscriptionStatus | null | undefined): boolean {
  return status === "active" || status === "trialing";
}

export async function getSubscriptionByUserId(
  userId: string,
): Promise<StoredSubscription | null> {
  if (useFileStore()) {
    const store = await readFileStore();
    return store.byUserId[userId] ?? null;
  }

  return getMemoryStore().get(userId) ?? null;
}

export async function getSubscriptionByCustomerId(
  customerId: string,
): Promise<StoredSubscription | null> {
  if (useFileStore()) {
    const store = await readFileStore();
    const userId = store.byCustomerId[customerId];
    if (!userId) {
      return null;
    }
    return store.byUserId[userId] ?? null;
  }

  const userId = getCustomerIndex().get(customerId);
  if (!userId) {
    return null;
  }
  return getMemoryStore().get(userId) ?? null;
}

export async function upsertSubscription(input: {
  user_id: string;
  email?: string | null;
  stripe_customer_id: string;
  stripe_subscription_id: string;
  status: SubscriptionStatus;
  current_period_end?: string | null;
}): Promise<StoredSubscription> {
  const record: StoredSubscription = {
    user_id: input.user_id,
    email: input.email ?? null,
    stripe_customer_id: input.stripe_customer_id,
    stripe_subscription_id: input.stripe_subscription_id,
    status: input.status,
    current_period_end: input.current_period_end ?? null,
    updated_at: new Date().toISOString(),
  };

  if (useFileStore()) {
    const store = await readFileStore();
    store.byUserId[record.user_id] = record;
    store.byCustomerId[record.stripe_customer_id] = record.user_id;
    await writeFileStore(store);
    return record;
  }

  getMemoryStore().set(record.user_id, record);
  getCustomerIndex().set(record.stripe_customer_id, record.user_id);
  return record;
}

export async function updateSubscriptionByCustomerId(
  customerId: string,
  patch: {
    status?: SubscriptionStatus;
    stripe_subscription_id?: string;
    current_period_end?: string | null;
    email?: string | null;
  },
): Promise<StoredSubscription | null> {
  const existing = await getSubscriptionByCustomerId(customerId);
  if (!existing) {
    return null;
  }

  return upsertSubscription({
    user_id: existing.user_id,
    email: patch.email !== undefined ? patch.email : existing.email,
    stripe_customer_id: existing.stripe_customer_id,
    stripe_subscription_id: patch.stripe_subscription_id ?? existing.stripe_subscription_id,
    status: patch.status ?? existing.status,
    current_period_end:
      patch.current_period_end !== undefined
        ? patch.current_period_end
        : existing.current_period_end,
  });
}
