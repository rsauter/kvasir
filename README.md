# Kvasir – KI-Unterstützung für Unihockey-Vereine

Kvasir bringt deiner KI bei, für Vorstand und Funktionäre eines Unihockey-Vereins zu recherchieren
und Entwürfe zu schreiben. Das Paket enthält:

- **Rollen** für Präsidium, Kassier, Nachwuchs, Spielbetrieb, Sponsoring und einen Texter
- **Arbeitsabläufe** für Reglementsrecherche, Vorstandsanträge und Stelleninserate
- **Regeln**: Quellen nennen, nichts erfinden, Datenschutz, Entwürfe kennzeichnen
- **Wissen**: alle wichtigen Erlasse von Swiss Unihockey und kantonale Quellen (zurzeit Kanton Bern:
  Sport- und Lotteriefonds), jeweils mit Stand und Link zum Original

Du brauchst nichts zu installieren. Es sind reine Textdateien.

**Neuestes Paket herunterladen:** [Releases](../../releases/latest) → `kvasir-<datum>.zip`

## Variante A: KI im Browser (ChatGPT, Copilot, Claude, Euria usw.)

1. ZIP entpacken und den Ordner `upload/` öffnen.
2. Diese Dateien in den Chat hochladen:
   - `kvasir.md` (immer)
   - `sources.md` (immer)
   - `knowledge-swissunihockey.md` (Reglemente von Swiss Unihockey)
   - `knowledge-canton-be.md` (nur für Vereine im Kanton Bern)
   - optional: Statuten oder Reglemente deines Vereins
3. Schreiben: «Lies kvasir.md und halte dich daran. Ich bin Kassier.» Dann deine Frage stellen.

Tipp: Wenn deine KI Projekte, eigene GPTs oder Agents kennt, lade die Dateien dort einmal hoch.
Dann musst du das nicht in jedem Chat wiederholen.

Gratisversionen haben weniger Platz und verarbeiten grosse Dateien teils nur auszugsweise. Wenn
Antworten unvollständig wirken, lade nur die Datei hoch, die zur Frage passt.

## Variante B: KI-Agent mit Ordnerzugriff (zum Beispiel Claude Code in VS Code)

1. ZIP entpacken, zum Beispiel nach `C:\kvasir`.
2. Ordner im Editor öffnen.
3. Im Chat schreiben: «Ich bin der Kassier. Welche Gebühren stellt der Verband für Lizenzen in Rechnung?»

Die KI liest `AGENTS.md` und lädt selbst, was sie braucht. Dokumente deines Vereins legst du in
`knowledge/club/` ab (siehe README dort).

## Was dein Verein selbst ergänzt

- **Eigene Dokumente** wie Statuten, Reglemente und Konzepte. Kvasir liefert sie nicht mit, weil sie jedem Verein gehören.
- **Eigene Regeln**, falls nötig, in `rules/club-*.md`. Sie dürfen die Kvasir-Regeln nur verschärfen.

## Fehlt dein Kanton?

Kantonale Förderung (Sportfonds, Lotteriefonds) ist in jedem Kanton anders geregelt. Zurzeit ist
nur der Kanton Bern enthalten. Melde dich bei der Kontaktperson unten und nenne die offiziellen
Seiten oder Leitfäden deines Kantons. Dann kommen sie in ein nächstes Paket.

## Wichtig

- Gib keine Personendaten von Mitgliedern ein, besonders nicht von Kindern und Jugendlichen.
- Gratisversionen von KI-Diensten können Eingaben speichern oder auswerten. Prüfe die
  Datenschutzeinstellungen deines Dienstes.
- Prüfe wichtige Antworten im Original. Die Links stehen bei jeder Quelle.
- Entwürfe nach aussen gibt der Vorstand frei.
- Kvasir gibt keine Rechtsberatung.

## Mitmachen

Neue Quellen, etwa die Leitfäden deines Kantons, Fehler oder Wünsche bitte als Issue melden.
Wer die Inhalte pflegen will, findet die Werkzeuge und den Ablauf in `tools/README.md`.
Zu den Rechten an den enthaltenen Texten siehe `NOTICE.md`.

## Stand und Kontakt

Der Stand steht im Namen des ZIP und am Anfang von `upload/kvasir.md`. Wenn sich Reglemente
ändern, gibt es ein neues Paket. Ersetze dann alle Dateien.

Kontakt und Pflege: (einsetzen)
# kvasir
