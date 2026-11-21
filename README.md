
GammaOS Pico Kids – KONKR Pocket Advance
Inoffizielle Modifikation von GammaOS Pico für den KONKR Pocket Advance mit vereinfachter Spieleoberfläche. Dieses Projekt ist nicht mit dem ursprünglichen GammaOS-Pico-Entwickler verbunden.

Status: Experimentelle Community-Version. Der Ersteller hat die modifizierte Firmware auf seinem eigenen KONKR Pocket Advance gestartet und die Oberfläche als funktionierend gemeldet (November 2026). Keine umfassende Hardware- oder Sicherheitstestreihe. Nicht für KONKR Pocket Block oder andere Geräte.

Was die Kids-Modifikation verändert
Im Standarddesign „Current“ bleiben Games und Resume erreichbar.
Der Hauptmenüpunkt Settings wird ausgeblendet; L/R führt nicht dorthin.
Der Menüeintrag Boot to Android wird entfernt und der entsprechende Aufruf deaktiviert.
Das Standarddesign „Current“ wird bevorzugt.
Spiele, Speichern/Laden und Resume sollen weiterhin funktionieren.
Was NICHT gesperrt ist
Dies ist keine vollständige Kindersicherung:

Android kann bei entfernter microSD-Karte oder über bestimmte Starttastenkombinationen weiterhin gestartet werden.
Ein fehlgeschlagener SD-Start kann einen Android-Rückfall ermöglichen.
In-Game-Emulatoreinstellungen sind weiterhin erreichbar.
Der technische Rückfall auf „Classic“ kann zusätzliche Optionsmenüs sichtbar machen.
microSD-Inhalte können außerhalb des Geräts verändert werden.
Empfehlung: Android zusätzlich mit einer PIN schützen und testen, ob diese beim Kaltstart abgefragt wird.

Kompatibilität und Risiko
Nur KONKR Pocket Advance. Nicht auf anderen Geräten flashen.
Bootloader-Flashing kann das Gerät unbrauchbar machen. Vorher beide Bootloader-Partitionen lk_a und lk_b sichern und Wiederherstellung prüfen.
Akku laden, USB-Verbindung beim Flashen nicht unterbrechen.
Bootloader-Image und mitgelieferte sdcard-Dateien als zusammengehöriges Paar verwenden; idealerweise eine separate microSD-Karte.
Die Emulator-Cores stammen teilweise aus Ersatz-Commits, weil die vom Upstream-Projekt referenzierten Commits beim Build nicht abrufbar waren. Kompatibilität kann abweichen.
Keine ROMs und keine BIOS-Dateien enthalten. Bitte nur Dateien verwenden, deren Nutzung und Verteilung zulässig sind.
Bauen
Das Repository enthält apply_kids_patch.py und .github/workflows/build-gammaos-pico-kids.yml. Der GitHub-Actions-Workflow lädt die Originalquellen, wendet die Kids-Modifikation an und erstellt ein experimentelles Paket aus Firmware-Image und SD-Karten-Dateien.

Repository auf GitHub öffnen und zu Actions wechseln.
Den Workflow auswählen und starten (soweit der Workflow einen manuellen Start vorsieht).
Nach erfolgreichem Build die Datei unter Artifacts herunterladen.
Das Build-Archiv und den Wiederherstellungsweg vor einem Flashvorgang prüfen.
Die GitHub-Actions-Builds verwenden teils nicht exakt die ursprünglich gepinnten Emulator-Versionen. Ein grüner Build garantiert keine Gerätekompatibilität.

Installation und Wiederherstellung
Für Backup, Update und Restore ausschließlich die offiziellen, gerätespezifischen Anleitungen und das GammaOS Pico Tool verwenden. Keinen Firmware-Flash ohne Backup und funktionierenden Rettungsweg durchführen.

GammaOS Pico (Originalprojekt)
GammaOS Pico Tool
Originalquellcode für den KONKR Pocket Advance
Offizielle Aktualisierung / Wiederherstellung
Credits und Lizenzen
Diese Modifikation baut auf der Arbeit von TheGammaSqueeze und den jeweiligen Emulator-Entwicklern auf. Der Bootloader und die Emulator-Cores sind nicht vollständig Eigenentwicklungen dieses Repositories.

Vor der Veröffentlichung eines kompilierten Firmware-Archivs müssen die Lizenz- und Weitergabebedingungen aller enthaltenen Bestandteile geprüft und die notwendigen Lizenztexte und Copyright-Hinweise beigefügt werden. Insbesondere unterliegt Snes9x einer eigenen Lizenz mit Einschränkungen für kommerzielle Nutzung; die Bedingungen gelten auch für abgeleitete Binärdistributionen. Keine proprietären ROMs/BIOS-Dateien beifügen. Eine eigene, pauschale Lizenz für sämtliche Fremdbestandteile wäre irreführend.

Snes9x-Pico / Lizenz
Snes9x-Lizenztext
English / Short summary
Unofficial, experimental GammaOS Pico Kids modification for KONKR Pocket Advance only. Hides the main Settings tab and removes the menu-based “Boot to Android” action. This is not a security boundary: Android can still be reached via other boot paths, in-game settings remain available, and flashing a bootloader is risky. Back up both lk_a and lk_b and verify recovery before flashing. Not affiliated with the original project. No ROMs or BIOS files included.





