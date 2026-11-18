#!/usr/bin/env python3
"""GammaOS Pico Kids (Konkr Pocket Advance): restrict bootloader UI.

Source: https://github.com/TheGammaSqueeze/lk-mt6785
Branch: lk-gba-emu-sd-card-kpa (reviewed 2026-11-18)
Changes only the two known C files; fails closed if source differs.
This script DOES NOT flash a device or touch its SD card.
"""
from pathlib import Path
import argparse
import sys


def replace_once(text: str, old: str, new: str, label: str) -> str:
    n = text.count(old)
    if n != 1:
        raise ValueError(f"{label}: expected 1 exact source occurrence, found {n}. "
                         "Upstream may have changed: no file is written.")
    return text.replace(old, new, 1)


def build_changes(root: Path) -> dict[Path, str]:
    fcur = root / "emu/gba/pico_current.c"
    fsnes = root / "emu/gba/gba_snes_menu.c"
    if not fcur.is_file() or not fsnes.is_file():
        raise ValueError("Expected emu/gba/pico_current.c and emu/gba/gba_snes_menu.c. "
                         "Specify the root of the lk-mt6785 source repository.")

    cur = fcur.read_text(encoding="utf-8")
    snes = fsnes.read_text(encoding="utf-8")
    if "GAMMAOS_PICO_KIDS_PATCH" in cur or "GAMMAOS_PICO_KIDS_PATCH" in snes:
        raise ValueError("Kids patch already applied: refusing to apply twice.")

    # Current theme, main menu tabs: do not render or navigate to Settings.
    cur = replace_once(
        cur,
        'static void rail(void)\n{\n\tstatic const char *label[3] = { "Games", "Resume", "Settings" };\n'
        '\tfloat pitch = s_uw * .116f < 148 ? s_uw * .116f : 148, yy = 119, x = s_p;\n'
        '\tint i;\n\tfor (i = 0; i < 3; i++) {',
        'static void rail(void)\n{\n\t/* GAMMAOS_PICO_KIDS_PATCH: only Games and Resume are visible. */\n'
        '\tstatic const char *label[3] = { "Games", "Resume", "Settings" };\n'
        '\tfloat pitch = s_uw * .116f < 148 ? s_uw * .116f : 148, yy = 119, x = s_p;\n'
        '\tint i;\n\tfor (i = 0; i < 2; i++) {',
        "hide Settings tab visually",
    )
    cur = replace_once(
        cur,
        'if (rb && S.tab < 2) { S.tab++; S.dip = .45f; }',
        'if (rb && S.tab < TAB_RESUME) { S.tab++; S.dip = .45f; }',
        "hide Settings tab from shoulder navigation",
    )
    cur = replace_once(
        cur,
        'if (S.sys >= S.nsys) S.sys = 0;',
        '/* If an earlier session was on Settings, leave it on Games instead. */\n'
        '\tif (S.tab > TAB_RESUME) { S.tab = TAB_GAMES; S.set_page = SPAGE_MAIN; }\n'
        '\tif (S.sys >= S.nsys) S.sys = 0;',
        "clamp restored tab state",
    )
    # Remove Boot to Android from Settings rows as a second line of defense.
    cur = replace_once(
        cur,
        '\t  SET_BOOT_OS, SET_ABOUT, -1 },',
        '\t  SET_ABOUT, -1 },',
        "remove Android row from settings list",
    )
    cur = replace_once(
        cur,
        'if (it == SET_BOOT_OS && ea) ayaneo_boot_to_os();   /* never returns */',
        '/* GAMMAOS_PICO_KIDS_PATCH: no Android boot action through Settings. */',
        "disable Android action in Current theme",
    )
    # Use Current even if an older SD setting selected Classic. Classic stays as fallback.
    snes = replace_once(
        snes,
        'if (gba_menu_theme() == snes_hash("current")) {',
        'if (1) { /* GAMMAOS_PICO_KIDS_PATCH: always try restricted Current menu. */',
        "force restricted Current theme",
    )
    snes = replace_once(
        snes,
        '\t\tif (snes_menu_take_sysreset(&s_menu)) {\n'
        '\t\t\textern void ayaneo_boot_to_os(void);\n'
        '\t\t\tayaneo_boot_to_os();   /* never returns */\n'
        '\t\t}',
        '\t\tif (snes_menu_take_sysreset(&s_menu)) {\n'
        '\t\t\t/* GAMMAOS_PICO_KIDS_PATCH: never boot Android via Classic fallback. */\n'
        '\t\t}',
        "disable Android action in Classic fallback",
    )
    return {fcur: cur, fsnes: snes}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("source_root", type=Path, nargs="?", default=Path("."),
                    help="root folder of lk-mt6785 source tree")
    ap.add_argument("--check", action="store_true", help="check patch anchors without writing")
    args = ap.parse_args()
    try:
        changes = build_changes(args.source_root.resolve())
        if args.check:
            print("OK: source matches expected GammaOS Pico code; patch can be applied.")
            return 0
        # All changes are computed in memory before any file is written.
        for file, new_text in changes.items():
            file.with_suffix(file.suffix + ".pre-kids.bak").write_bytes(file.read_bytes())
            file.write_text(new_text, encoding="utf-8")
            print("Patched:", file)
        print("Done. This is SOURCE ONLY: not compiled, not flashed, not device-tested.")
        return 0
    except Exception as e:
        print("ERROR:", e, file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
