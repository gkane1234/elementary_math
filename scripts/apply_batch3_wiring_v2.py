"""Wire remaining batch3 entries with precise catalog patching."""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys_path = ROOT
import sys

sys.path.insert(0, str(ROOT))

from scripts.apply_batch3_wiring import WIRING, CATALOG_FILES, STUB_TEMPLATE, create_stub


def wire_entry(catalog_path: Path, type_id: str, generator: str) -> bool:
    text = catalog_path.read_text(encoding="utf-8")
    if f'"{type_id}"' not in text:
        return False

    # _g6/_pa/_a2/_geo/_pc single-line call containing the id
    pattern = rf'(_\w+\([^)]*"{re.escape(type_id)}"[^)]*)(\))'
    m = re.search(pattern, text)
    if not m:
        # algebra_1 entry() multiline
        pattern2 = rf'("{re.escape(type_id)}",\s*\n\s+"[^"]+",\s*\n\s+"[^"]+",)(\s*\n)'
        m2 = re.search(pattern2, text)
        if not m2:
            print(f"FAIL pattern: {type_id}")
            return False
        chunk = text[m2.start() : m2.end() + 200]
        if re.search(rf'generator="{re.escape(generator)}"', chunk):
            return False
        if re.search(r'generator="(?!scaffold")[^"]+"', chunk):
            print(f"SKIP has generator: {type_id}")
            return False
        new_text = text[: m2.start(2)] + f'\n        generator="{generator}",' + text[m2.start(2) :]
        catalog_path.write_text(new_text, encoding="utf-8")
        return True

    chunk = m.group(0)
    if re.search(rf'generator="{re.escape(generator)}"', chunk):
        return False
    if re.search(r'generator="(?!scaffold")[^"]+"', chunk):
        print(f"SKIP has generator: {type_id}")
        return False

    inner = m.group(1)
    if "generator=" in inner:
        new_inner = re.sub(r'generator="scaffold"', f'generator="{generator}"', inner, count=1)
    else:
        new_inner = inner + f', generator="{generator}"'
    new_text = text[: m.start(1)] + new_inner + text[m.end(1) :]
    catalog_path.write_text(new_text, encoding="utf-8")
    return True


def main() -> None:
    wired = 0
    for type_id, generator, course, chapter in WIRING:
        if wire_entry(CATALOG_FILES[course], type_id, generator):
            create_stub(course, chapter, type_id)
            wired += 1
            print(f"WIRED {type_id} -> {generator}")
    print(f"Total: {wired}")


if __name__ == "__main__":
    main()
