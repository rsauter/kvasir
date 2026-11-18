#!/usr/bin/env python3
"""Holt PDF-Quellen (Leitfäden, Merkblätter) und legt sie als Volltext in knowledge/fulltext/<modul>/ ab.
Das Modul steht pro Dokument in tools/pdf-sources.json (zum Beispiel canton-be, canton-zh).

Welche PDFs dazugehören, steht in tools/pdf-sources.json.
Braucht pdftotext (xpdf oder poppler). Unter Windows liegt es bei Git for Windows bei.

Aufruf (im Hauptordner):
  python tools/fetch_pdfs.py            alle PDFs holen und umwandeln
  python tools/fetch_pdfs.py <id> ...   nur diese
  python tools/fetch_pdfs.py --check    nur prüfen, ob sich ein PDF geändert hat (schreibt nichts)
"""
import datetime
import hashlib
import json
import re
import shutil
import subprocess
import sys
import tempfile
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CONFIG = json.loads((ROOT / "tools" / "pdf-sources.json").read_text(encoding="utf-8"))
OUT_DIR = ROOT / "knowledge" / "fulltext"
SOURCES = ROOT / "knowledge" / "sources.md"
MARK_START, MARK_END = "<!-- pdf:start -->", "<!-- pdf:end -->"

GAP = re.compile(r"\S(\s{3,})(?=\S)")
HEADING = re.compile(r"^(\d+(?:\.\d+)*)\.?\s{2,}(\S.*)$")
DEEP_HEADING = re.compile(r"^(\d+(?:\.\d+){2,})\s+([A-ZÄÖÜ].*)$")
LIST_MARK = re.compile(r"^([−\-–•▪]|o(?=\s)|[a-z]\)|[ivx]+\.|\d+\.|\d+\))\s+")
BULLET_ONLY = re.compile(r"^([−\-–•▪]|[a-z]\)|[ivx]+\.|\d+\.|\d+\))$")


# ---------- PDF holen und Text ziehen ----------

def find_pdftotext() -> str:
    for cand in ("pdftotext", r"C:\Program Files\Git\ucrt64\bin\pdftotext.exe",
                 r"C:\Program Files\Git\mingw64\bin\pdftotext.exe"):
        path = shutil.which(cand) or (cand if Path(cand).exists() else None)
        if path:
            return path
    sys.exit("pdftotext nicht gefunden. Git for Windows installieren oder poppler/xpdf in den PATH legen.")


def download(url: str) -> bytes:
    req = urllib.request.Request(url, headers={"User-Agent": "kvasir-fetch/1.0"})
    with urllib.request.urlopen(req, timeout=60) as res:
        return res.read()


def pdf_pages(data: bytes) -> list[list[str]]:
    with tempfile.TemporaryDirectory() as tmp:
        pdf = Path(tmp) / "in.pdf"
        pdf.write_bytes(data)
        txt = Path(tmp) / "out.txt"
        subprocess.run([find_pdftotext(), "-table", "-enc", "UTF-8", "-q", str(pdf), str(txt)], check=True)
        raw = txt.read_text(encoding="utf-8", errors="replace")
    pages = [p.split("\n") for p in raw.split("\f")]
    return [[l.rstrip() for l in p] for p in pages if any(l.strip() for l in p)]


# ---------- Seitenköpfe, Fusszeilen, Inhaltsverzeichnis ----------

def strip_furniture(pages: list[list[str]]) -> tuple[list[str], str]:
    cover = " ".join(l.strip() for l in pages[0] if l.strip())
    stand = (re.search(r"\b(\d{2}/\d{4})\b", cover) or [None, ""])[1]
    body_pages = pages[1:]
    nonempty = [[l for l in p if l.strip()] for p in body_pages]
    first_words = [p[0].split()[0] for p in nonempty if p]
    common_first = max(set(first_words), key=first_words.count) if first_words else None
    second_lines = [p[1].strip() for p in nonempty if len(p) > 1]
    common_second = max(set(second_lines), key=second_lines.count) if second_lines else None
    out = []
    for p in nonempty:
        lines = list(p)
        if lines and common_first and lines[0].split()[0] == common_first:
            lines.pop(0)
            if lines and lines[0].strip() == common_second:
                lines.pop(0)
        if lines and re.search(r"\b\d+/\d+\s*$", lines[-1]):
            lines.pop()
        out.extend(lines)
    # Inhaltsverzeichnis entfernen
    try:
        start = next(i for i, l in enumerate(out) if l.strip() == "Inhaltsverzeichnis")
        last_toc = max(i for i, l in enumerate(out) if re.search(r"\.{5,}\s*\d+\s*$", l))
        out = out[:start] + out[last_toc + 1:]
    except (StopIteration, ValueError):
        pass
    return out, stand


# ---------- Text zu Markdown ----------

def indent(line: str) -> int:
    return len(line) - len(line.lstrip())


def gaps(line: str) -> list[int]:
    """Spaltenanfänge innerhalb der Zeile (nach mindestens drei Leerzeichen)."""
    return [m.end(1) for m in GAP.finditer(line)]


def join_lines(parts: list[str]) -> str:
    text = ""
    for p in parts:
        p = p.strip()
        if not p:
            continue
        if not text:
            text = p
        elif text.endswith("-") and not text.endswith(" -") and p[:1].islower() and not re.match(r"(und|oder|bzw)\b", p):
            text = text[:-1] + p                                   # Silbentrennung
        elif text.endswith("-") and not text.endswith(" -"):
            text = text + p                                        # Bindestrich-Wort
        else:
            text = text + " " + p
    return re.sub(r"\s{2,}", " ", text)


def paragraphs(lines: list[str]) -> list[str]:
    """Fliesstext-Zeilen zu Absätzen und Listen zusammenfügen."""
    if not lines:
        return []
    width = max(len(l.rstrip()) for l in lines)
    base = min(indent(l) for l in lines if l.strip())
    blocks, cur, cur_indent, cur_list = [], [], 0, False

    def flush():
        nonlocal cur
        if cur:
            text = join_lines(cur)
            if cur_list:
                m = LIST_MARK.match(cur[0])
                level = max(0, (cur_indent - base) // 4)
                marker = m.group(1)
                rest = join_lines([cur[0][m.end():], *cur[1:]])
                text = f"{'  ' * level}- {'' if marker in '−-–•▪o' else marker + ' '}{rest}"
            blocks.append((cur_list, text))
        cur = []

    prev = ""
    for l in lines:
        s = l.strip()
        if not s:
            continue
        ind = indent(l)
        is_item = bool(LIST_MARK.match(s))
        if is_item:
            flush()
            cur, cur_indent, cur_list = [s], ind, True
        elif cur_list and (ind > cur_indent or cur[-1].endswith('-')):
            cur.append(s)                                          # Fortsetzung des Listenpunkts
        else:
            ends = prev.rstrip().endswith((".", ":", "!", "?", ")", "»")) and len(prev.rstrip()) < width * 0.8
            if cur_list or not cur or ends:
                flush()
                cur, cur_indent, cur_list = [s], ind, False
            else:
                cur.append(s)
        prev = l
    flush()
    md = []
    for i, (is_list, text) in enumerate(blocks):
        if i and not (is_list and blocks[i - 1][0]):
            md.append("")
        md.append(text)
    return md


def split_columns(line: str, starts: list[int]) -> list[str]:
    cells = []
    for i, st in enumerate(starts):
        end = starts[i + 1] if i + 1 < len(starts) else len(line)
        cells.append(line[st:end] if len(line) > st else "")
    # Text, der knapp vor dem Spaltenanfang beginnt, der richtigen Spalte zuordnen
    return cells


def table_md(rows: list[list[list[str]]]) -> list[str]:
    cells = [[join_lines(c).replace("|", "/") for c in r] for r in rows]
    n = max(len(r) for r in cells)
    cells = [r + [""] * (n - len(r)) for r in cells]
    out = ["| " + " | ".join(cells[0]) + " |", "|" + " --- |" * n]
    out += ["| " + " | ".join(r) + " |" for r in cells[1:]]
    return out


def to_markdown(lines: list[str]) -> str:
    md: list[str] = []
    i, n = 0, len(lines)
    text_buf: list[str] = []

    def flush_text():
        nonlocal text_buf
        if text_buf:
            md.extend(["", *paragraphs(text_buf), ""])
        text_buf = []

    while i < n:
        line = lines[i]
        s = line.strip()
        if not s:
            i += 1
            continue
        dh = DEEP_HEADING.match(line) if not HEADING.match(line) else None
        if dh and indent(line) == 0:
            flush_text()
            col = line.index(dh.group(2))
            # Sperrsatz-Artefakte wie «Teilnah   me» zusammenfügen, sonst Lücke = Leerzeichen
            title = re.sub(r"(\w)\s{3,}([a-zäöü]{1,2}\b)", r"\1\2", dh.group(2))
            parts = [title]
            i += 1
            while i < n and lines[i].strip() and abs(indent(lines[i]) - col) <= 1 and not gaps(lines[i].strip()):
                parts.append(lines[i]); i += 1
            level = min(dh.group(1).count('.') + 2, 6)
            md.extend(['', f"{'#' * level} {dh.group(1)} {join_lines(parts)}", ''])
            continue
        h = HEADING.match(line)
        g = gaps(line)
        # Überschrift: Nummer am linken Rand, keine weiteren Spalten
        if h and indent(line) == 0:
            # ausserhalb von Tabellen ist eine nummerierte Zeile am linken Rand eine Überschrift,
            # auch wenn der Blocksatz Lücken in den Titel setzt
            flush_text()
            col = line.index(h.group(2))
            title = [re.sub(r"(\w)\s{3,}([a-zäöü]{1,2}\b)", r"\1\2", h.group(2))]
            i += 1
            while i < n and lines[i].strip() and indent(lines[i]) == col and not gaps(lines[i].strip()):
                title.append(lines[i]); i += 1
            level = min(h.group(1).count(".") + 2, 6)
            md.extend(["", f"{'#' * level} {h.group(1)} {join_lines(title)}", ""])
            continue
        # Tabelle mit drei oder mehr Spalten: Kopfzeile mit mindestens zwei Lücken am linken Rand
        header_cells = [c.strip() for c in split_columns(line, [0] + g)] if g else []
        if indent(line) == 0 and len(g) >= 2 and all(len(c) <= 30 for c in header_cells):
            flush_text()
            starts = [0] + g
            rows: list[list[list[str]]] = []
            while i < n:
                l = lines[i]
                if not l.strip():
                    i += 1; continue
                if indent(l) == 0 and not gaps(l) and rows:
                    break
                hm = HEADING.match(l) or DEEP_HEADING.match(l)
                if hm and indent(l) == 0 and l.index(hm.group(2)) < starts[1] - 2:
                    break                                          # Überschrift beendet die Tabelle
                cells = split_columns(l, starts)
                if cells[0].strip() or not rows:
                    rows.append([[c] for c in cells])
                else:
                    for k, c in enumerate(cells):
                        rows[-1][k].append(c)
                i += 1
            md.extend(["", *table_md(rows), ""])
            continue
        # Randstichwort mit Inhalt rechts (zweispaltiger Abschnitt)
        if indent(line) == 0 and g and not BULLET_ONLY.match(line[:g[0]].strip()) and len(line[:g[0]].strip()) <= 25:
            flush_text()
            col = g[0]
            start_i = i
            sections: list[tuple[list[str], list[str]]] = []
            while i < n:
                l = lines[i]
                if not l.strip():
                    i += 1; continue
                lg = gaps(l)
                if indent(l) == 0 and DEEP_HEADING.match(l) and i > start_i:
                    break
                if indent(l) == 0:
                    label_part = l[:col].strip() if (lg and lg[0] == col) or len(l) <= col else None
                    if label_part is None or HEADING.match(l) and not lg:
                        if lg and abs(lg[0] - col) <= 2:
                            label_part = l[:lg[0]].strip()
                        else:
                            break
                    content = l[col:] if len(l) > col else ""
                    if sections and (sections[-1][0][-1].endswith("-") or (content.strip()[:1].islower() and sections[-1][1])):
                        sections[-1][0].append(label_part)
                    else:
                        sections.append(([label_part], []))
                    if content.strip():
                        sections[-1][1].append(" " * col + content.strip() if not content.startswith(" ") else l[col:].rjust(len(l[col:])))
                elif indent(l) >= col - 2:
                    if not sections:
                        break
                    sections[-1][1].append(l)
                else:
                    break
                i += 1
            if i == start_i:                                       # nichts erkannt: als Fliesstext behandeln
                text_buf.append(line)
                i += 1
                continue
            for label, content in sections:
                body = paragraphs([c if indent(c) >= col else " " * col + c.strip() for c in content])
                md.extend(["", f"**{join_lines(label)}**", "", *body, ""])
            continue
        text_buf.append(line)
        i += 1
    flush_text()
    text = "\n".join(md)
    return re.sub(r"\n{3,}", "\n\n", text).strip()


# ---------- Dateien ----------

def header_value(path: Path, key: str) -> str | None:
    if not path.exists():
        return None
    m = re.search(rf"^{re.escape(key)}: (.*)$", path.read_text(encoding="utf-8")[:3000], re.M)
    return m.group(1).strip() if m else None


def doc_path(doc: dict) -> Path:
    """Volltexte liegen pro Modul in einem eigenen Ordner, zum Beispiel fulltext/canton-be/."""
    return OUT_DIR / doc["module"] / f"{doc['id']}.md"


def write_doc(doc: dict, data: bytes, today: str) -> tuple[Path, str]:
    pages = pdf_pages(data)
    lines, stand = strip_furniture(pages)
    body = to_markdown(lines)
    path = doc_path(doc)
    path.parent.mkdir(parents=True, exist_ok=True)
    head = [
        f"Quelle: {doc['title']}",
        f"Herausgeber: {doc['publisher']}",
        f"Link: {doc['page']}",
        f"PDF: {doc['pdf']}",
        f"Stand/Gültig ab: {stand or '(im PDF nicht gefunden)'}",
        f"Ausgezogen am: {today} von: tools/fetch_pdfs.py (automatisch, Volltext)",
        f"PDF-SHA256: {hashlib.sha256(data).hexdigest()}",
        f"Bereich: {doc['scope']}",
        f"Relevant für: {', '.join(doc['agents'])}",
        "",
        "> Automatisch aus dem PDF umgewandelt. Tabellen und Randstichworte können ungenau sein.",
        "> Massgebend ist das PDF unter dem Link oben.",
        "",
        f"# {doc['title']}",
        "",
        body,
        "",
    ]
    path.write_text("\n".join(head), encoding="utf-8")
    return path, stand


def write_sources(rows: list[dict]) -> None:
    md = SOURCES.read_text(encoding="utf-8")
    block = "\n".join([
        MARK_START,
        "<!-- Dieser Block wird von tools/fetch_pdfs.py erzeugt. Nicht von Hand ändern. -->",
        "",
        "| Modul | Dokument | Herausgeber | Bereich | Relevant für | Stand | Volltext |",
        "|---|---|---|---|---|---|---|",
        *[f"| {r['module']} | [{r['title']}]({r['pdf']}) | {r['publisher']} | {r['scope']} | {', '.join(r['agents'])} | {r['stand']} | `fulltext/{r['module']}/{r['id']}.md` |" for r in rows],
        "",
        MARK_END,
    ])
    s, e = md.find(MARK_START), md.find(MARK_END)
    md = md[:s] + block + md[e + len(MARK_END):] if s >= 0 and e > s else md.rstrip() + "\n\n" + block + "\n"
    SOURCES.write_text(md, encoding="utf-8")


def main() -> None:
    args = sys.argv[1:]
    check = "--check" in args
    only = [a for a in args if not a.startswith("--")]
    docs = CONFIG["documents"]
    unknown = [o for o in only if o not in {d["id"] for d in docs}]
    if unknown:
        sys.exit(f"Nicht in tools/pdf-sources.json: {', '.join(unknown)}")
    today = datetime.date.today().isoformat()
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    rows, changed = [], 0
    for doc in docs:
        path = doc_path(doc)
        if only and doc["id"] not in only:
            if path.exists():
                rows.append({**doc, "stand": header_value(path, "Stand/Gültig ab") or ""})
            continue
        try:
            data = download(doc["pdf"])
        except Exception as err:  # noqa: BLE001
            print(f"! {doc['id']:36} Fehler: {err}")
            changed += 1
            if path.exists():
                rows.append({**doc, "stand": header_value(path, "Stand/Gültig ab") or ""})
            continue
        new = header_value(path, "PDF-SHA256") != hashlib.sha256(data).hexdigest()
        status = "neu" if not path.exists() else "GEÄNDERT" if new else "unverändert"
        changed += new
        if check:
            print(f"{'*' if new else ' '} {doc['id']:36} {status}")
            continue
        _, stand = write_doc(doc, data, today)
        rows.append({**doc, "stand": stand})
        print(f"{'*' if new else ' '} {doc['id']:36} {status:12} Stand {stand}")
    if check:
        print(f"\n{changed} PDF(s) neu oder geändert. Mit «python tools/fetch_pdfs.py» aktualisieren." if changed else "\nAlles aktuell.")
        sys.exit(1 if changed else 0)
    write_sources(rows)
    print("\nknowledge/fulltext/ und knowledge/sources.md nachgeführt.")


if __name__ == "__main__":
    main()
