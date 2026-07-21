"use client";

import { useCallback, useEffect, useState } from "react";
import { Modal } from "@/components/Modal";

type FlatRow = {
  path: string;
  value: unknown;
  type: "number" | "bool" | "string" | "string_list";
};

type KnobsResponse = {
  path?: string;
  knobs?: Record<string, unknown>;
  flat?: FlatRow[];
  error?: string;
};

export function DifficultyKnobsDebug() {
  const [open, setOpen] = useState(false);
  const [loading, setLoading] = useState(false);
  const [status, setStatus] = useState("");
  const [filePath, setFilePath] = useState("");
  const [rows, setRows] = useState<FlatRow[]>([]);
  const [draft, setDraft] = useState<Record<string, unknown>>({});
  const [raw, setRaw] = useState("");
  const [showRaw, setShowRaw] = useState(false);

  const load = useCallback(async () => {
    setLoading(true);
    setStatus("Loading…");
    try {
      const res = await fetch("/api/debug/difficulty-knobs");
      const data = (await res.json()) as KnobsResponse;
      if (!res.ok) throw new Error(data.error || res.statusText);
      setFilePath(data.path || "");
      setRows(data.flat || []);
      setRaw(JSON.stringify(data.knobs ?? {}, null, 2));
      const next: Record<string, unknown> = {};
      for (const row of data.flat || []) {
        next[row.path] =
          row.type === "string_list" && Array.isArray(row.value)
            ? (row.value as string[]).join(", ")
            : row.value;
      }
      setDraft(next);
      setStatus("Loaded");
    } catch (err) {
      setStatus(err instanceof Error ? err.message : "Failed to load");
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    if (open) void load();
  }, [open, load]);

  const saveUpdates = async () => {
    setLoading(true);
    setStatus("Saving…");
    try {
      const updates: Record<string, unknown> = {};
      for (const row of rows) {
        const rawVal = draft[row.path];
        if (row.type === "bool") updates[row.path] = Boolean(rawVal);
        else if (row.type === "string_list") {
          updates[row.path] = String(rawVal ?? "")
            .split(",")
            .map((s) => s.trim())
            .filter(Boolean);
        } else {
          const n = Number(rawVal);
          updates[row.path] = Number.isFinite(n) ? n : rawVal;
        }
      }
      const res = await fetch("/api/debug/difficulty-knobs", {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ updates }),
      });
      const data = (await res.json()) as KnobsResponse;
      if (!res.ok) throw new Error(data.error || res.statusText);
      setRows(data.flat || []);
      setRaw(JSON.stringify(data.knobs ?? {}, null, 2));
      setStatus("Saved — new worksheets use updated knobs");
    } catch (err) {
      setStatus(err instanceof Error ? err.message : "Failed to save");
    } finally {
      setLoading(false);
    }
  };

  const saveRaw = async () => {
    setLoading(true);
    setStatus("Saving raw…");
    try {
      const knobs = JSON.parse(raw) as Record<string, unknown>;
      const res = await fetch("/api/debug/difficulty-knobs", {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ knobs }),
      });
      const data = (await res.json()) as KnobsResponse;
      if (!res.ok) throw new Error(data.error || res.statusText);
      setRows(data.flat || []);
      setRaw(JSON.stringify(data.knobs ?? {}, null, 2));
      const next: Record<string, unknown> = {};
      for (const row of data.flat || []) {
        next[row.path] =
          row.type === "string_list" && Array.isArray(row.value)
            ? (row.value as string[]).join(", ")
            : row.value;
      }
      setDraft(next);
      setStatus("Raw JSON saved");
    } catch (err) {
      setStatus(err instanceof Error ? err.message : "Failed to save raw");
    } finally {
      setLoading(false);
    }
  };

  return (
    <>
      <button
        type="button"
        className="debug-fab"
        onClick={() => setOpen(true)}
        title="Difficulty knobs debug"
      >
        Debug
      </button>

      <Modal
        open={open}
        title="Difficulty knobs (debug)"
        onClose={() => setOpen(false)}
        footer={
          <div className="debug-knobs-footer">
            <button type="button" className="secondary" onClick={() => void load()} disabled={loading}>
              Reload
            </button>
            <button type="button" onClick={() => void saveUpdates()} disabled={loading}>
              Save
            </button>
          </div>
        }
      >
        <p className="debug-knobs-meta">
          <code>{filePath || "difficulty_knobs.json"}</code>
          {status ? <span className="debug-knobs-status"> — {status}</span> : null}
        </p>
        <div className="debug-knobs-table-wrap">
          <table className="debug-knobs-table">
            <thead>
              <tr>
                <th>Path</th>
                <th>Value</th>
              </tr>
            </thead>
            <tbody>
              {rows.map((row) => (
                <tr key={row.path}>
                  <td>
                    <code>{row.path}</code>
                  </td>
                  <td>
                    {row.type === "bool" ? (
                      <input
                        type="checkbox"
                        checked={Boolean(draft[row.path])}
                        onChange={(e) =>
                          setDraft((prev) => ({ ...prev, [row.path]: e.target.checked }))
                        }
                      />
                    ) : (
                      <input
                        type={row.type === "number" ? "number" : "text"}
                        step="any"
                        value={String(draft[row.path] ?? "")}
                        onChange={(e) =>
                          setDraft((prev) => ({
                            ...prev,
                            [row.path]:
                              row.type === "number" ? e.target.valueAsNumber || e.target.value : e.target.value,
                          }))
                        }
                      />
                    )}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
        <details
          className="debug-knobs-raw"
          open={showRaw}
          onToggle={(e) => setShowRaw((e.target as HTMLDetailsElement).open)}
        >
          <summary>Raw JSON</summary>
          <textarea
            value={raw}
            onChange={(e) => setRaw(e.target.value)}
            spellCheck={false}
            rows={14}
          />
          <button type="button" className="secondary" onClick={() => void saveRaw()} disabled={loading}>
            Save raw JSON
          </button>
        </details>
      </Modal>
    </>
  );
}
