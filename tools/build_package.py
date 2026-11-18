#!/usr/bin/env python3
"""Baut das Kvasir-Paket für alle Vereine und alle Rollen.

Aufruf (im Hauptordner):
  python tools/build_package.py              Version = heutiges Datum
  python tools/build_package.py 2026-12-01   Version selbst setzen

Ergebnis: dist/kvasir-<version>.zip mit
  README.md     Anleitung für die Nutzerinnen und Nutzer
  upload/       wenige Dateien für KIs im Browser (ChatGPT, Copilot, Claude, Euria …)
  AGENTS.md …   der ganze Ordner für KI-Agenten wie Claude Code (ohne tools/)

Nicht ins Paket kommen: tools/, dist/, rules.local.md, Vereins- und Ressortregeln
(rules/club-*, rules/department-*) und eigene Dokumente in knowledge/club/ ausser dem README.
"""
import datetime
import re
import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DIST = ROOT / "dist"
KNOWLEDGE = ROOT / "knowledge"


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8").strip()


def parse_agent(path: Path) -> tuple[dict, str]:
    m = re.match(r"^---\n(.*?)\n---\n(.*)$", read(path), re.S)
    if not m:
        sys.exit(f"Kopfzeilen fehlen in {path}")
    meta = {}
    for line in m.group(1).splitlines():
        key, _, val = line.partition(":")
        meta[key.strip()] = val.strip()
    meta["skills"] = [s.strip() for s in meta.get("skills", "").strip("[]").split(",") if s.strip()]
    return meta, m.group(2).strip()


def demote(text: str, levels: int) -> str:
    """Überschriften um `levels` Stufen tiefer setzen (ausserhalb von Codeblöcken)."""
    out, fence = [], False
    for line in text.splitlines():
        if line.startswith("```"):
            fence = not fence
        if not fence and re.match(r"^#{1,6} ", line):
            hashes = len(line) - len(line.lstrip("#"))
            line = "#" * min(hashes + levels, 6) + line[hashes:]
        out.append(line)
    return "\n".join(out)


def core_rules() -> list[Path]:
    return sorted(p for p in (ROOT / "rules").glob("0*.md"))


def knowledge_bundles() -> dict[str, list[Path]]:
    """Ein Upload-Paket pro Modul in knowledge/fulltext/ plus die Auszüge."""
    bundles = {}
    for module in sorted(p for p in (KNOWLEDGE / "fulltext").iterdir() if p.is_dir()):
        files = sorted(module.glob("*.md"))
        if files:
            bundles[module.name] = files
    excerpts = sorted(p for p in (KNOWLEDGE / "excerpts").glob("*.md") if p.name != "README.md")
    if excerpts:
        bundles["excerpts"] = excerpts
    return bundles


# ---------- upload/kvasir.md ----------

def build_instructions(version: str, bundles: dict[str, list[Path]]) -> str:
    agents = [parse_agent(p) for p in sorted((ROOT / "agents").glob("*.md"))]
    roles = [(m, b) for m, b in agents if m.get("type") != "maintenance"]
    used_skills = sorted({s for m, _ in roles for s in m["skills"]})
    files = ["`kvasir.md` (diese Datei)", "`sources.md` (Quellenliste)"] + [f"`knowledge-{k}.md`" for k in bundles]

    parts = [
        f"# Kvasir – Anweisung für die KI (Stand {version})",
        "Du bist eine KI, die Vorstandsmitglieder und Funktionäre eines Unihockey-Vereins in der Schweiz "
        "bei Recherche und Entwürfen unterstützt. Halte dich an die Regeln, die Rolle und die Arbeitsabläufe "
        "in dieser Datei. Antworte auf Deutsch, per Du, mit Schweizer Schreibweise (ss statt ß).",
        "## Beiliegende Dateien",
        "Die Person hat dir diese Dateien gegeben: " + ", ".join(files) + ". "
        "Dazu kommen eventuell Dokumente ihres Vereins (Statuten, Reglemente).",
        "Pfadangaben in dieser Anweisung beziehen sich auf den Kvasir-Ordner. So findest du sie in den Dateien:\n"
        "- `knowledge/sources.md` → `sources.md`\n"
        + "\n".join(f"- `knowledge/fulltext/{k}/…` → `knowledge-{k}.md`, Abschnitt «Datei: …»" for k in bundles if k != "excerpts")
        + ("\n- `knowledge/excerpts/…` → `knowledge-excerpts.md`" if "excerpts" in bundles else "")
        + "\n- `knowledge/club/…` → die Dokumente, die die Person von ihrem Verein hochgeladen hat\n"
        "- `rules/…`, `skills/…` → die Abschnitte «Regeln» und «Arbeitsabläufe» unten",
        "Fehlt eine Datei, die du brauchst, sag das und bitte die Person, sie hochzuladen.",
        "## Start jeder Sitzung",
        "1. Ist nicht klar, welche Funktion die Person hat, frage: «Welche Funktion hast du?» Mögliche Rollen:\n"
        + "\n".join(f"   - {m['title']} (`{m['name']}`)" for m, _ in roles)
        + "\n   Passt keine Rolle genau, nimm die nächstliegende und sag, welche du gewählt hast.\n"
        "2. Arbeite dann in dieser Rolle, mit ihren Schwerpunktquellen und Arbeitsabläufen.\n"
        "3. Hängt eine Antwort vom Kanton ab (zum Beispiel Beiträge aus Sport- oder Lotteriefonds), frage nach "
        "dem Kanton des Vereins. Liegt für diesen Kanton keine Datei `knowledge-canton-<kürzel>.md` bei, sag das "
        "offen und nenne die zuständige kantonale Stelle. Übertrage keine Regeln eines anderen Kantons.",
        "# Regeln, die immer gelten",
        *[demote(read(r), 1) for r in core_rules()],
        "# Rollen",
    ]
    for meta, body in roles:
        parts.append(f"## Rolle: {meta['title']} (`{meta['name']}`)")
        parts.append(f"Arbeitsabläufe dieser Rolle: {', '.join(f'`{s}`' for s in meta['skills'])}")
        parts.append(demote(re.sub(r"^# Agent: .*\n", "", body), 1))
    parts.append("# Arbeitsabläufe")
    for skill in used_skills:
        parts.append(f"<!-- Skill: {skill} -->")
        parts.append(demote(read(ROOT / "skills" / f"{skill}.md"), 1))
    return "\n\n".join(parts) + "\n"


def build_bundle(name: str, files: list[Path], version: str) -> str:
    titles = {"swissunihockey": "Erlasse von Swiss Unihockey", "excerpts": "Ausgewählte Auszüge"}
    title = titles.get(name, f"Kantonale Quellen ({name.removeprefix('canton-').upper()})" if name.startswith("canton-") else name)
    parts = [
        f"# Kvasir-Wissen: {title} (Paket {version})",
        "Jeder Abschnitt «Datei: …» enthält ein Dokument mit Kopf (Quelle, Link, Stand). "
        "Nenne in Antworten das Dokument, den Artikel und den Stand aus diesem Kopf.",
        f"Prüfdatum: Alle Dokumente dieser Datei wurden für das Paket {version} auf neue Fassungen geprüft. "
        "Dieses Datum zählt für die Aktualität, nicht «Ausgezogen am».",
    ]
    for f in files:
        rel = f.relative_to(ROOT).as_posix()
        parts.append(f"---\n\n# Datei: {rel}\n\n" + demote(read(f), 1))
    return "\n\n".join(parts) + "\n"


# ---------- Paket ----------

def package_files() -> list[Path]:
    files = [ROOT / "README.md", ROOT / "NOTICE.md", ROOT / "AGENTS.md", ROOT / "CLAUDE.md"]
    files += sorted((ROOT / "agents").glob("*.md"))
    files += sorted((ROOT / "skills").glob("*.md"))
    files += core_rules()
    files += [KNOWLEDGE / "sources.md", KNOWLEDGE / "club" / "README.md"]
    files += sorted((KNOWLEDGE / "excerpts").glob("*.md"))
    files += sorted((KNOWLEDGE / "fulltext").rglob("*.md"))
    return [f for f in files if f.exists()]


def main() -> None:
    version = sys.argv[1] if len(sys.argv) > 1 else datetime.date.today().isoformat()
    DIST.mkdir(exist_ok=True)
    bundles = knowledge_bundles()
    top = f"kvasir-{version}"
    out = DIST / f"{top}.zip"
    upload = {
        "kvasir.md": build_instructions(version, bundles),
        "sources.md": read(KNOWLEDGE / "sources.md") + "\n",
        **{f"knowledge-{k}.md": build_bundle(k, v, version) for k, v in bundles.items()},
    }
    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as z:
        for name, text in upload.items():
            z.writestr(f"{top}/upload/{name}", text)
        for f in package_files():
            z.write(f, f"{top}/{f.relative_to(ROOT).as_posix()}")
    print(f"{out.relative_to(ROOT).as_posix()} erstellt")
    for name, text in upload.items():
        print(f"  upload/{name:34} {len(text.encode('utf-8')) // 1024:>5} KB")
    print(f"  dazu {len(package_files())} Dateien für KI-Agenten wie Claude Code")


if __name__ == "__main__":
    main()
