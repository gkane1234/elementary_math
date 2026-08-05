"""Extract poly_rating_calc_derivatives from Chromium LevelDB (log + blocks)."""
from __future__ import annotations

import json
import shutil
import struct
from collections import Counter
from pathlib import Path

SRC = Path.home() / "AppData/Roaming/Cursor/Partitions/cursor-browser/Local Storage/leveldb"
TMP = Path.home() / "AppData/Local/Temp/poly_rating_ls_full"
OUT_DIR = Path(__file__).resolve().parent
OUT_RATINGS = OUT_DIR / "calc_derivatives_ratings.json"
OUT_RAW = OUT_DIR / "_extracted_localStorage.json"

KEY = b"poly_rating_calc_derivatives"
BLOCK_SIZE = 32768

# LevelDB log record types
FULL, FIRST, MIDDLE, LAST = 1, 2, 3, 4


def copy_db() -> None:
    TMP.mkdir(parents=True, exist_ok=True)
    for p in SRC.iterdir():
        try:
            shutil.copy2(p, TMP / p.name)
        except Exception as e:
            print(f"skip {p.name}: {e}")


def read_varint(buf: bytes, i: int) -> tuple[int, int]:
    result = 0
    shift = 0
    while i < len(buf):
        b = buf[i]
        i += 1
        result |= (b & 0x7F) << shift
        if (b & 0x80) == 0:
            return result, i
        shift += 7
        if shift > 63:
            raise ValueError("varint too long")
    raise ValueError("truncated varint")


def iter_log_records(raw: bytes) -> list[bytes]:
    """Reassemble logical records from a LevelDB .log file."""
    records: list[bytes] = []
    buf = bytearray()
    pos = 0
    n = len(raw)
    while pos + 7 <= n:
        # Skip trailer padding to next block
        block_off = pos % BLOCK_SIZE
        if block_off > BLOCK_SIZE - 7:
            pos += BLOCK_SIZE - block_off
            continue
        _crc, length, rtype = struct.unpack_from("<IHB", raw, pos)
        pos += 7
        if length == 0 and rtype == 0:
            # padding
            pos += BLOCK_SIZE - (pos % BLOCK_SIZE) if pos % BLOCK_SIZE else 0
            continue
        if pos + length > n:
            break
        data = raw[pos : pos + length]
        pos += length
        if rtype == FULL:
            records.append(data)
        elif rtype == FIRST:
            buf = bytearray(data)
        elif rtype == MIDDLE:
            buf.extend(data)
        elif rtype == LAST:
            buf.extend(data)
            records.append(bytes(buf))
            buf = bytearray()
        else:
            # unknown — reset fragment
            buf = bytearray()
    return records


def values_from_write_batch(batch: bytes) -> list[bytes]:
    """Parse LevelDB WriteBatch for Put values whose key contains KEY."""
    # WriteBatch: 8-byte seq + 4-byte count + entries
    if len(batch) < 12:
        return []
    values: list[bytes] = []
    i = 12
    while i < len(batch):
        tag = batch[i]
        i += 1
        if tag == 1:  # put
            try:
                klen, i = read_varint(batch, i)
                key = batch[i : i + klen]
                i += klen
                vlen, i = read_varint(batch, i)
                val = batch[i : i + vlen]
                i += vlen
            except Exception:
                break
            if KEY in key:
                values.append(val)
        elif tag == 0:  # delete
            try:
                klen, i = read_varint(batch, i)
                i += klen
            except Exception:
                break
        else:
            break
    return values


def value_to_obj(val: bytes) -> dict | None:
    payload = val
    if payload[:1] in (b"\x00", b"\x01") and len(payload) > 1:
        payload = payload[1:]
    for dec in ("utf-8", "utf-16-le"):
        try:
            text = payload.decode(dec)
        except Exception:
            continue
        text = text.lstrip("\ufeff").strip()
        if not text.startswith("{"):
            j = text.find("{")
            if j < 0:
                continue
            text = text[j:]
        try:
            obj = json.loads(text)
        except Exception:
            try:
                obj, _ = json.JSONDecoder().raw_decode(text)
            except Exception:
                continue
        if isinstance(obj, dict) and obj:
            return obj
    return None


def score(obj: dict) -> tuple[int, int]:
    rated = sum(
        1 for v in obj.values() if isinstance(v, dict) and v.get("rating_1_to_5") is not None
    )
    return rated, len(obj)


def main() -> None:
    copy_db()
    best: dict | None = None
    best_score = (-1, -1)

    log_path = TMP / "000014.log"
    raw = log_path.read_bytes()
    records = iter_log_records(raw)
    print(f"log logical records: {len(records)}")
    for ri, rec in enumerate(records):
        if KEY not in rec and b"calc_deriv_" not in rec:
            continue
        vals = values_from_write_batch(rec)
        if not vals and KEY in rec:
            # fallback: value immediately after key+varint inside record
            j = rec.find(KEY)
            i = j + len(KEY)
            try:
                vlen, k = read_varint(rec, i)
                vals = [rec[k : k + vlen]]
            except Exception:
                vals = []
        for val in vals:
            obj = value_to_obj(val)
            if obj is None:
                print(f"  record {ri}: value len={len(val)} parse fail head={val[:50]!r}")
                continue
            sc = score(obj)
            print(f"  record {ri}: entries={sc[1]} rated={sc[0]}")
            if sc > best_score:
                best = obj
                best_score = sc

    if best is None:
        raise SystemExit("FAILED: no ratings object recovered")

    OUT_RAW.write_text(json.dumps(best, indent=2), encoding="utf-8")
    OUT_RATINGS.write_text(json.dumps(best, indent=2), encoding="utf-8")
    hist = Counter(
        v["rating_1_to_5"]
        for v in best.values()
        if isinstance(v, dict) and v.get("rating_1_to_5") is not None
    )
    nullish = sum(
        1 for v in best.values() if isinstance(v, dict) and v.get("rating_1_to_5") is None
    )
    print(f"WROTE {OUT_RATINGS}")
    print(f"entries={len(best)} rated={best_score[0]} visited_null={nullish}")
    print(f"score_hist={dict(sorted(hist.items()))}")


if __name__ == "__main__":
    main()
