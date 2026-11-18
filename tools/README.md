# Kvasir pflegen

Dieser Ordner ist nur für die Person, die Kvasir pflegt. Er kommt nicht ins Paket für die Vereine.

## Voraussetzungen

| Werkzeug | Wofür |
|---|---|
| Python 3.12 oder neuer | `fetch_pdfs.py`, `build_package.py` |
| Node.js 18 oder neuer | `fetch_tlex.mjs` |
| `pdftotext` (xpdf oder poppler, bei Git for Windows dabei) | PDF-Umwandlung in `fetch_pdfs.py` |

## Ablauf für ein neues Paket

```
node tools/fetch_tlex.mjs --check     # neue Fassungen bei Swiss Unihockey?
python tools/fetch_pdfs.py --check    # geänderte PDF-Leitfäden?

node tools/fetch_tlex.mjs             # falls ja: neu holen
python tools/fetch_pdfs.py

python tools/build_package.py         # Paket bauen: dist/kvasir-<datum>.zip
```

Vor dem Verteilen:
- Änderungen in `knowledge/fulltext/` kurz durchsehen, besonders bei neuen PDF-Fassungen. Die Umwandlung ist heuristisch.
- Bestehende Auszüge in `knowledge/excerpts/` prüfen, wenn sich der zugrunde liegende Erlass geändert hat.

## Quellen ergänzen

| Was | Wo eintragen |
|---|---|
| Weiterer Erlass von Swiss Unihockey | `tools/tlex-sources.json` (`node tools/fetch_tlex.mjs --list` zeigt alle) |
| PDF-Leitfaden, zum Beispiel ein weiterer Kanton | `tools/pdf-sources.json` mit `"module": "canton-<kürzel>"` |

Danach in `knowledge/sources.md` die Übersicht ergänzen und einen kurzen Abschnitt über dem
generierten Block schreiben (siehe Bern als Beispiel). Der Agent `librarian` beschreibt die
Schritte ausführlich.

## Was ins Paket kommt

`build_package.py` packt:
- `upload/`: `kvasir.md` (alle Regeln, Rollen und Abläufe), `sources.md` und pro Modul eine
  Wissensdatei (`knowledge-swissunihockey.md`, `knowledge-canton-be.md`, …)
- den Ordner für KI-Agenten: `AGENTS.md`, `CLAUDE.md`, `agents/`, `skills/`, `rules/0*.md`, `knowledge/`

Nicht ins Paket kommen `tools/`, `dist/`, `rules.local.md`, `rules/club-*.md`,
`rules/department-*.md` und eigene Vereinsdokumente in `knowledge/club/` (nur deren README).

## GitHub

| Workflow | Auslöser | Was er tut |
|---|---|---|
| `.github/workflows/update-sources.yml` | montags und von Hand | Prüft TLex und PDFs. Neue Swiss-Unihockey-Fassungen kommen als Pull Request, geänderte PDFs als Issue. |
| `.github/workflows/release.yml` | Tag `v*`, zum Beispiel `v2026.11.18` | Prüft, ob alles aktuell ist, baut das Paket und hängt es an ein Release. |

Damit der Prüf-Workflow Pull Requests eröffnen darf: Repository → Settings → Actions → General →
«Allow GitHub Actions to create and approve pull requests» einschalten.

Neues Release:

```
git tag v2026.11.18
git push origin v2026.11.18
```
