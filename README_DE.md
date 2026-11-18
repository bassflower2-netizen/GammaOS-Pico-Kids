# GammaOS Pico Kids – experimenteller Quellcode-Patch für KONKR Pocket Advance

**Stand: 18.11.2026 – kein fertig kompiliertes Image, nicht auf echter Hardware getestet.**

**Was dieser Patch verändert (GammaOS Pico, Branch `lk-gba-emu-sd-card-kpa`):**

- Im Standarddesign „Current“ sind nur **Games** und **Resume** als Register sichtbar.
- L/R kann nicht zu „Settings“ navigieren. Auch ein aus einer vorherigen Sitzung gespeicherter Settings-Zustand wird auf „Games“ gesetzt.
- Der Eintrag „Boot to Android“ wird aus der Settings-Liste entfernt; sein Aufruf wird zusätzlich deaktiviert.
- Das Standarddesign „Current“ wird bevorzugt, selbst wenn auf der Karte zuvor „Classic“ gewählt war.
- Im technischen Rückfall auf das Classic-Design ist der dortige „Boot to Android“-Aufruf ebenfalls deaktiviert. **Die weiteren Classic-Optionsmenüs sind beim Fallback noch sichtbar.**
- Die Spielbibliothek, Spiele, Savegames und Resume bleiben erhalten. Das In-Game-Menü zum Speichern/Laden und zum Einstellen der Emulatoren bleibt erhalten; eine vollständige Sperre aller Spieloptionen ist dies nicht.

## WICHTIG: Keine vollständige Kindersicherung

- **Ohne microSD-Karte bootet das Gerät weiterhin Android.** Das ist ein wichtiger Notfall-Rückweg des Projekts.
- **SELECT + START beim Einschalten** kann weiterhin Android auswählen.
- Bei ungültigen Kartendaten oder Fehlern kann der Bootloader nach Android zurückfallen.
- **Unbedingt Android mit einer PIN sperren**, und prüfen, dass sie nach einem Kaltstart abgefragt wird. Die PIN allein ist keine Absicherung der SD-Kartendaten gegen Zugriff am PC.
- Nicht die Rettungswege aus dem Bootloader entfernen: Damit erhöht sich das Brick-Risiko.
- Ein falsches Bootloader-Image kann das Gerät unbrauchbar machen. **Nicht flashen, bevor ein vollständiges Backup des Original-Bootloaders und ein Wiederherstellungsweg vorhanden sind.**

## Variante A: Lokal patchen / kompilieren (Linux x86-64)

In einer Linux-x86-64-Umgebung die offiziellen Sourcen laden:

```bash
git clone --recursive --single-branch -b lk-gba-emu-sd-card-kpa https://github.com/TheGammaSqueeze/lk-mt6785.git
cd lk-mt6785
python3 /PFAD/ZUM/apply_kids_patch.py . --check
python3 /PFAD/ZUM/apply_kids_patch.py .
./build_konkr_kpa.sh
```

Laut Upstream benötigt der Build Linux, Python 3 mit Pillow und numpy, OpenSSL sowie `arm-none-eabi-gcc`/`g++` für die Emulator-Cores. Der LK selbst nutzt eine mitgelieferte Toolchain. Es müssen auch die Submodule vorhanden sein.

Das Ergebnis wäre bei erfolgreichem Build `out/lk_a_kpa_signed.img` und `out/sdcard/`. Es wurde **hier nicht erstellt oder auf dem Handheld getestet**.

**Hinweis für Snapdragon-/ARM64-Windows/WSL:** Im offiziellen Repository ist die LK-Toolchain vorgegeben; für ARM64-WSL ist die Ausführbarkeit der enthaltenen Host-Compiler nicht nachgewiesen. Besser zunächst über GitHub Actions auf x86-64 Linux bauen (Variante B).

## Variante B: Über GitHub Actions bauen (ohne lokale Linux-x86-64-Maschine)

1. Auf GitHub ein **privates** neues Repository anlegen.
2. `apply_kids_patch.py`, `README_DE.md` und `.github/workflows/build-gammaos-pico-kids.yml` an **denselben Positionen** aus dieser ZIP-Datei in das neue Repo hochladen.
3. Im Repository zu **Actions → GammaOS Pico Kids - build (experimental) → Run workflow** gehen.
4. Wenn der Build erfolgreich durchläuft, unter dem Workflowlauf bei **Artifacts** die ZIP `GammaOS-Pico-Kids-KPA-UNTESTED` laden.
5. **Nur nach Backup und sorgfältiger Prüfung** das darin enthaltene Image als Firmware-Update verwenden. Keine Blind-Flashes. Die GitHub-Actions-Pipeline ist ein **ungetesteter Buildvorschlag**, keine Garantie für einen erfolgreichen Build.

Für die Aktualisierung eines Handhelds, auf dem GammaOS Pico bereits installiert ist, ausschließlich die zum **KONKR Pocket Advance** gehörende, dokumentierte Update-/Restore-Methode von GammaOS Pico verwenden. Keinesfalls `Pocket Block`-Images oder Anleitungen zum erstmaligen Flashen unbesehen für ein Update übernehmen.

## Quelle

- Offizielle Releases und Warnungen: https://github.com/TheGammaSqueeze/GammaOSPico
- Original-Quellcode: https://github.com/TheGammaSqueeze/lk-mt6785/tree/lk-gba-emu-sd-card-kpa
- Offizielles Update/Wiederherstellung: https://github.com/TheGammaSqueeze/GammaOSPico/wiki/Updating-and-Going-Back

**Lizenzhinweis:** Dieses Archiv enthält keinen Original-Bootloader, keine Firmware-Binärdateien, keine ROMs und keine BIOS-Dateien – nur einen Python-Patcher, eine experimentelle Build-Automation und diese Anleitung. Die Lizenzen der Upstream-Quellen gelten unverändert.
