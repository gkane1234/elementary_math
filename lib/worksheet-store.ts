import { promises as fs } from "fs";
import path from "path";
import { randomUUID } from "crypto";
import type { WorksheetDraft } from "@/lib/types";

export type StoredWorksheet = {
  id: string;
  created_at: string;
  title: string;
  full_data: WorksheetDraft;
  paid: boolean;
  stripe_session_id?: string | null;
  user_email?: string | null;
};

const DATA_DIR = path.join(process.cwd(), ".data");
const DATA_FILE = path.join(DATA_DIR, "worksheets.json");

declare global {
  // eslint-disable-next-line no-var
  var __worksheetStore: Map<string, StoredWorksheet> | undefined;
}

function getMemoryStore(): Map<string, StoredWorksheet> {
  if (!global.__worksheetStore) {
    global.__worksheetStore = new Map();
  }
  return global.__worksheetStore;
}

function useFileStore(): boolean {
  return process.env.NODE_ENV === "development" || process.env.WORKSHEET_STORE_FILE === "true";
}

async function readFileStore(): Promise<Record<string, StoredWorksheet>> {
  try {
    const raw = await fs.readFile(DATA_FILE, "utf-8");
    return JSON.parse(raw) as Record<string, StoredWorksheet>;
  } catch {
    return {};
  }
}

async function writeFileStore(data: Record<string, StoredWorksheet>): Promise<void> {
  await fs.mkdir(DATA_DIR, { recursive: true });
  await fs.writeFile(DATA_FILE, JSON.stringify(data, null, 2), "utf-8");
}

async function readRecord(id: string): Promise<StoredWorksheet | null> {
  if (useFileStore()) {
    const store = await readFileStore();
    return store[id] ?? null;
  }

  return getMemoryStore().get(id) ?? null;
}

async function writeRecord(record: StoredWorksheet): Promise<void> {
  if (useFileStore()) {
    const store = await readFileStore();
    store[record.id] = record;
    await writeFileStore(store);
    return;
  }

  getMemoryStore().set(record.id, record);
}

export async function createWorksheet(
  title: string,
  fullData: WorksheetDraft,
): Promise<StoredWorksheet> {
  const record: StoredWorksheet = {
    id: `ws_${randomUUID().replace(/-/g, "").slice(0, 16)}`,
    created_at: new Date().toISOString(),
    title,
    full_data: fullData,
    paid: false,
  };

  await writeRecord(record);
  return record;
}

export async function getWorksheet(id: string): Promise<StoredWorksheet | null> {
  return readRecord(id);
}

export async function markWorksheetPaid(
  id: string,
  stripeSessionId: string,
  userEmail?: string | null,
): Promise<StoredWorksheet | null> {
  const record = await readRecord(id);
  if (!record) {
    return null;
  }

  const updated: StoredWorksheet = {
    ...record,
    paid: true,
    stripe_session_id: stripeSessionId,
    user_email: userEmail ?? record.user_email ?? null,
  };

  await writeRecord(updated);
  return updated;
}
