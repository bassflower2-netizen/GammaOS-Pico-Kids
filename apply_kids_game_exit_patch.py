#!/usr/bin/env python3
"""GammaOS Pico Kids v0.2: AYA/Menu single press -> normal game exit.

Targets the KONKR Pocket Advance SD-boot firmware branch
TheGammaSqueeze/lk-mt6785: lk-gba-emu-sd-card-kpa.

The patch is deliberately fail-closed: it checks exact known source anchors
before writing any file and rejects an already-patched tree.
It does NOT flash firmware and has not been device tested.
"""

from __future__ import annotations

import argparse
from pathlib import Path
import re
import sys

MARKER = "GAMMAOS_PICO_KIDS_ONE_TAP_EXIT"


def patch_gba(source: str) -> str:
    """Preserve the GBA driver's existing s_close_req -> save/exit path."""
    anchor = re.compile(
        r"(?m)^(?P<indent>[ \t]*)if \(aya_edge\(\)\)[ \t]*\n"
        r"[ \t]*gba_igm_toggle\(\);[ \t]*$"
    )
    hits = list(anchor.finditer(source))
    if len(hits) != 1 or "if (s_close_req)" not in source:
        raise ValueError("GBA: expected exactly one AYA toggle and the normal close handler")
    indent = hits[0].group("indent")
    return anchor.sub(
        lambda m: f"{indent}/* {MARKER}: skip overlay; use normal save-and-close path. */\n"
                  f"{indent}if (aya_edge())\n"
                  f"{indent}\ts_close_req = 1;",
        source,
        count=1,
    )


def patch_aya_block(source: str, label: str, exit_code: str) -> str:
    """Replace only physical AYA tap's overlay-open block, not the exit/cleanup code.

    All four SD runtimes contain one `if (aya && !aya_prev) { ... }` block
    followed by `aya_prev = aya;` which toggles Current / Classic IGMs.
    Verify that we found that specific block before replacing it.
    """
    opener = "if (aya && !aya_prev) {"
    terminator = "aya_prev = aya;"
    if source.count(opener) != 1:
        raise ValueError(f"{label}: expected one AYA tap handler, found {source.count(opener)}")
    start = source.index(opener)
    end = source.find(terminator, start)
    if end == -1 or end - start > 3000:
        raise ValueError(f"{label}: could not safely locate the end of the AYA handler")
    old = source[start:end]
    # This must be precisely the in-game overlay toggle, not a similarly
    # shaped control flow in another function.
    if "pico_igm_open(" not in old or "_menu_open" not in old:
        raise ValueError(f"{label}: AYA block does not match the known menu-opening path")
    if old.count("pico_igm_open(") != 1:
        raise ValueError(f"{label}: ambiguous AYA block; refusing to modify")
    # Keep the existing `aya_prev = aya;` assignment and existing hold and
    # normal exit teardown further down untouched.
    replacement = (
        f"/* {MARKER}: AYA tap returns to the selector; no in-game settings. */\n"
        f"if (aya && !aya_prev) {{\n"
        f"    {exit_code}\n"
        f"}}\n"
    )
    return source[:start] + replacement + source[end:]


def build_changes(root: Path) -> dict[Path, str]:
    paths = {
        "GBA": root / "emu/gba/gba_driver.c",
        "GB/GBC": root / "emu/gbc/gbc_sd_run.c",
        "SNES": root / "emu/snes9x/snes_sd_run.c",
        "Genesis": root / "emu/genesis/genesis_sd_run.c",
        "NES": root / "emu/nes/nes_sd_run.c",
    }
    for label, path in paths.items():
        if not path.is_file():
            raise ValueError(f"{label}: missing source file {path}")

    originals = {label: p.read_text(encoding="utf-8") for label, p in paths.items()}
    for label, code in originals.items():
        if MARKER in code:
            raise ValueError(f"{label}: the one-tap patch is already applied")

    result = {
        paths["GBA"]: patch_gba(originals["GBA"]),
        paths["GB/GBC"]: patch_aya_block(
            originals["GB/GBC"], "GB/GBC",
            "extern void gbc_menu_arm_reverse(const unsigned short *frame);\n"
            "    gbc_menu_arm_reverse(vbuf);\n"
            "    break;",
        ),
        paths["SNES"]: patch_aya_block(
            originals["SNES"], "SNES", "g_snes_menu_exit = 1;"
        ),
        paths["Genesis"]: patch_aya_block(
            originals["Genesis"], "Genesis", "g_genesis_menu_exit = 1;"
        ),
        paths["NES"]: patch_aya_block(
            originals["NES"], "NES", "g_nes_menu_exit = 1;"
        ),
    }
    for label, file in paths.items():
        updated = result[file]
        if updated == originals[label] or updated.count(MARKER) != 1:
            raise ValueError(f"{label}: expected exactly one effective patch")
    return result


def main() -> int:
    argp = argparse.ArgumentParser(description=__doc__)
    argp.add_argument("source_root", type=Path, nargs="?", default=Path("."))
    argp.add_argument("--check", action="store_true", help="check all source anchors without writing")
    args = argp.parse_args()
    try:
        changes = build_changes(args.source_root.resolve())
        if args.check:
            print("OK: all five in-game menu interceptors match the expected source. Nothing written.")
            return 0
        # Every source was read, checked and modified in memory first.
        for path, updated in changes.items():
            path.with_name(path.name + ".pre-one-tap.bak").write_bytes(path.read_bytes())
            path.write_text(updated, encoding="utf-8")
            print("Patched:", path.relative_to(args.source_root.resolve()))
        print("Done: one-tap Menu -> normal exit in GBA, GB/GBC, SNES, Genesis and NES.")
        print("SOURCE ONLY: must compile; NOT hardware-tested; do not flash without backup.")
        return 0
    except (OSError, UnicodeError, ValueError) as exc:
        print("ERROR:", exc, file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
