import { NextResponse } from "next/server";
import { promises as fs } from "fs";
import path from "path";

const KNOBS_REL = path.join(
  "question_engine",
  "frameworks",
  "primitives",
  "difficulty_knobs.json",
);

function knobsAbsolutePath() {
  return path.join(process.cwd(), KNOBS_REL);
}

type FlatRow = { path: string; value: unknown; type: "number" | "bool" | "string_list" };

function flatten(obj: unknown, prefix = ""): FlatRow[] {
  const rows: FlatRow[] = [];
  if (obj === null || obj === undefined) return rows;
  if (typeof obj === "boolean") {
    rows.push({ path: prefix, value: obj, type: "bool" });
    return rows;
  }
  if (typeof obj === "number") {
    rows.push({ path: prefix, value: obj, type: "number" });
    return rows;
  }
  if (Array.isArray(obj) && obj.every((x) => typeof x === "string")) {
    rows.push({ path: prefix, value: obj, type: "string_list" });
    return rows;
  }
  if (typeof obj === "object") {
    const record = obj as Record<string, unknown>;
    // Lane-style { min_d: n }
    if ("min_d" in record && Object.keys(record).every((k) => k === "min_d" || k === "label")) {
      rows.push({
        path: prefix ? `${prefix}.min_d` : "min_d",
        value: record.min_d,
        type: "number",
      });
      return rows;
    }
    for (const [key, val] of Object.entries(record)) {
      if (key.startsWith("_")) continue;
      const next = prefix ? `${prefix}.${key}` : key;
      rows.push(...flatten(val, next));
    }
  }
  return rows;
}

function setPath(root: Record<string, unknown>, dotted: string, value: unknown) {
  const parts = dotted.split(".").filter(Boolean);
  let cur: Record<string, unknown> = root;
  for (let i = 0; i < parts.length - 1; i++) {
    const part = parts[i]!;
    const next = cur[part];
    if (!next || typeof next !== "object" || Array.isArray(next)) {
      cur[part] = {};
    }
    cur = cur[part] as Record<string, unknown>;
  }
  cur[parts[parts.length - 1]!] = value;
}

export async function GET() {
  try {
    const filePath = knobsAbsolutePath();
    const text = await fs.readFile(filePath, "utf8");
    const knobs = JSON.parse(text) as Record<string, unknown>;
    return NextResponse.json({
      path: KNOBS_REL,
      knobs,
      flat: flatten(knobs),
    });
  } catch (error) {
    return NextResponse.json(
      { error: error instanceof Error ? error.message : "Failed to read knobs" },
      { status: 500 },
    );
  }
}

export async function PUT(request: Request) {
  try {
    const body = (await request.json()) as {
      knobs?: Record<string, unknown>;
      updates?: Record<string, unknown>;
    };
    const filePath = knobsAbsolutePath();
    let knobs: Record<string, unknown>;

    if (body.knobs && typeof body.knobs === "object") {
      knobs = body.knobs;
    } else if (body.updates && typeof body.updates === "object") {
      const text = await fs.readFile(filePath, "utf8");
      knobs = JSON.parse(text) as Record<string, unknown>;
      for (const [p, value] of Object.entries(body.updates)) {
        setPath(knobs, p, value);
      }
    } else {
      return NextResponse.json({ error: "Provide knobs or updates" }, { status: 400 });
    }

    await fs.writeFile(filePath, `${JSON.stringify(knobs, null, 2)}\n`, "utf8");
    return NextResponse.json({
      ok: true,
      path: KNOBS_REL,
      knobs,
      flat: flatten(knobs),
    });
  } catch (error) {
    return NextResponse.json(
      { error: error instanceof Error ? error.message : "Failed to save knobs" },
      { status: 500 },
    );
  }
}
