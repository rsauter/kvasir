#!/usr/bin/env node
// Holt Erlasse aus TLex (LexWork) und legt sie als Volltext in knowledge/fulltext/swissunihockey/ ab.
// Pflegt ausserdem den TLex-Block in knowledge/sources.md.
//
// Aufruf (im Hauptordner):
//   node tools/fetch_tlex.mjs           alle Erlasse aus tools/tlex-sources.json holen
//   node tools/fetch_tlex.mjs 3-10 4-1  nur diese Erlasse holen
//   node tools/fetch_tlex.mjs --check   nur prüfen, ob es neue Fassungen gibt (schreibt nichts)
//   node tools/fetch_tlex.mjs --list    alle Erlasse in TLex auflisten, auch nicht konfigurierte

import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const CONFIG = JSON.parse(fs.readFileSync(path.join(ROOT, "tools", "tlex-sources.json"), "utf8"));
const OUT_DIR = path.join(ROOT, "knowledge", "fulltext", "swissunihockey");
const SOURCES = path.join(ROOT, "knowledge", "sources.md");
const MARK_START = "<!-- tlex:start -->";
const MARK_END = "<!-- tlex:end -->";
const { base, lang } = CONFIG;

async function getJson(url) {
  const res = await fetch(url, { headers: { Accept: "application/json" } });
  if (!res.ok) throw new Error(`${res.status} bei ${url}`);
  return res.json();
}

const fetchDoc = (nr) => getJson(`${base}/api/${lang}/texts_of_law/${encodeURIComponent(nr)}/show_as_json`)
  .then((j) => j.text_of_law);

// ---------- HTML zu Markdown ----------

const ENTITIES = { nbsp: " ", amp: "&", lt: "<", gt: ">", quot: '"', apos: "'", shy: "",
  auml: "ä", ouml: "ö", uuml: "ü", Auml: "Ä", Ouml: "Ö", Uuml: "Ü", eacute: "é", egrave: "è",
  agrave: "à", ccedil: "ç", laquo: "«", raquo: "»", ndash: "–", mdash: "—", hellip: "…",
  rsquo: "’", lsquo: "‘", rdquo: "”", ldquo: "“", bdquo: "„", sect: "§", deg: "°", times: "×" };

function decode(s) {
  return s
    .replace(/&#(\d+);/g, (_, n) => String.fromCodePoint(+n))
    .replace(/&#x([0-9a-f]+);/gi, (_, n) => String.fromCodePoint(parseInt(n, 16)))
    .replace(/&([a-z]+);/gi, (m, n) => ENTITIES[n] ?? m);
}

function inline(html) {
  return decode(html
    .replace(/<strong>\s*\*\s*<\/strong>/g, "")          // Änderungsmarker von TLex
    .replace(/<br\s*\/?>/gi, " ")
    .replace(/<\/?(strong|b)>/gi, "**")
    .replace(/<\/?(em|i)>/gi, "_")
    .replace(/<sup[^>]*>.*?<\/sup>/gis, "")               // Fussnotenverweise
    .replace(/<[^>]+>/g, " "))
    .replace(/\*\*\s*\*\*/g, "")
    .replace(/[ \t\r\n]+/g, " ")
    .trim();
}

const pick = (v) => (v && typeof v === "object" ? v[lang] ?? Object.values(v)[0] : v) || "";

function table(html) {
  const rows = [...html.matchAll(/<tr[^>]*>(.*?)<\/tr>/gis)].map((r) =>
    [...r[1].matchAll(/<t[hd][^>]*>(.*?)<\/t[hd]>/gis)].map((c) => inline(c[1]).replace(/\|/g, "/")));
  if (!rows.length) return inline(html);
  const width = Math.max(...rows.map((r) => r.length));
  const line = (r) => `| ${Array.from({ length: width }, (_, i) => r[i] ?? "").join(" | ")} |`;
  return [line(rows[0]), `|${" --- |".repeat(width)}`, ...rows.slice(1).map(line)].join("\n");
}

function render(node, out, depth = 0) {
  if (Array.isArray(node)) return node.forEach((n) => render(n, out, depth));
  if (!node || typeof node !== "object") return;
  const html = pick(node.html_content);
  switch (node.type) {
    case "title": {
      const level = Number((html.match(/level_(\d+)/) || [])[1] || 1);
      const num = inline((html.match(/class='number'>(.*?)<\/span>/s) || [])[1] || "");
      const text = inline(pick(node.text)) || inline((html.match(/class='title_text'>(.*?)<\/span>/s) || [])[1] || "");
      if (num || text) out.push("", `${"#".repeat(Math.min(level + 1, 4))} ${[num, text].filter(Boolean).join(" ")}`, "");
      break;
    }
    case "article": {
      const num = inline(pick(node.number));
      const title = inline(pick(node.text));
      out.push("", `#### ${[num, title].filter(Boolean).join(" ")}`, "");
      break;
    }
    case "paragraph": {
      const num = inline((html.match(/^\s*<div class='paragraph'>\s*<span class='number'>(.*?)<\/span>/s) || [])[1] || "");
      const body = html.replace(/^\s*<div class='paragraph'>\s*<span class='number'>.*?<\/span>/s, "");
      const text = inline(body);
      if (text) out.push(num ? `(${num}) ${text}` : text, "");
      break;
    }
    case "enumeration": {
      const num = inline((html.match(/<td class='number'>(.*?)<\/td>/s) || [])[1] || "");
      const text = inline(html.replace(/<td class='number'>.*?<\/td>/s, ""));
      if (text) out.push(`${"  ".repeat(Math.max(depth - 1, 0))}- ${num ? num + " " : ""}${text}`);
      break;
    }
    case "table":
      out.push("", table(html), "");
      break;
    default: {
      const text = inline(html);
      if (text) out.push(text, "");
    }
  }
  const childDepth = node.type === "enumeration" ? depth + 1 : node.type === "paragraph" ? 1 : depth;
  if (node.children) render(node.children, out, childDepth);
  if (node.type === "paragraph" && node.children?.some((c) => c.type === "enumeration")) out.push("");
}

// ---------- Datei schreiben ----------

const slug = (s) => s.toLowerCase().replace(/[^a-z0-9.]+/g, "-").replace(/^-|-$/g, "");
const fileName = (nr, abbr) => `${CONFIG.filePrefix}-${nr.replace(/\./g, "_")}${abbr ? "-" + slug(abbr) : ""}.md`;
const stripAbbr = (t) => t.replace(/\s*\([A-Z0-9]+\)\s*$/, "");
const abbrOf = (tol) => tol.abbreviation || (tol.title.match(/\(([A-Z0-9]+)\)\s*$/) || [])[1] || "";

function readHeader(file) {
  if (!fs.existsSync(file)) return null;
  const head = fs.readFileSync(file, "utf8").slice(0, 2000);
  const get = (k) => (head.match(new RegExp(`^${k}: (.*)$`, "m")) || [])[1]?.trim();
  return { version: get("TLex-Version"), stand: get("Stand/Gültig ab"), fetched: get("Ausgezogen am") };
}

function existingFile(nr) {
  const prefix = `${CONFIG.filePrefix}-${nr.replace(/\./g, "_")}`;
  if (!fs.existsSync(OUT_DIR)) return null;
  const f = fs.readdirSync(OUT_DIR).find((n) => n === `${prefix}.md` || n.startsWith(`${prefix}-`));
  return f ? path.join(OUT_DIR, f) : null;
}

function toMarkdown(tol, entry, today) {
  const sv = tol.selected_version;
  let content = sv.json_content;
  if (typeof content === "string") content = JSON.parse(content);
  const doc = content.document ?? content;
  const body = [];
  render(doc.content ?? doc, body);
  const footer = inline(pick(doc.footer));
  if (footer) body.push("", "---", "", footer);
  const text = body.join("\n").replace(/\n{3,}/g, "\n\n").trim();
  return [
    `Quelle: ${tol.systematic_number} ${tol.title}`,
    `Herausgeber: ${CONFIG.publisher}`,
    `Link: ${tol.canonical_link}`,
    `PDF: ${tol.pdf_link}`,
    `Stand/Gültig ab: ${sv.version_dates_str}`,
    `Ausgezogen am: ${today} von: tools/fetch_tlex.mjs (automatisch, Volltext)`,
    `TLex-Version: ${sv.id}`,
    `Bereich: ${entry.scope}`,
    `Relevant für: ${entry.agents.join(", ")}`,
    "",
    `> Automatisch erzeugter Volltext. Massgebend ist das Original unter dem Link oben.`,
    "",
    `# ${tol.systematic_number} ${tol.title}`,
    "",
    text,
    "",
  ].join("\n");
}

// ---------- sources.md ----------

function sourcesBlock(rows) {
  const lines = [
    MARK_START,
    `<!-- Dieser Block wird von tools/fetch_tlex.mjs erzeugt. Nicht von Hand ändern. -->`,
    "",
    `Systematik: ${base}/app/${lang}/systematic/texts_of_law`,
    "",
    "| Nr. | Erlass | Bereich | Relevant für | Stand | Volltext |",
    "|---|---|---|---|---|---|",
    ...rows.map((r) => `| ${r.nr} | [${r.title}](${r.link}) | ${r.scope} | ${r.agents.join(", ")} | ${r.stand} | \`fulltext/swissunihockey/${r.file}\` |`),
    "",
    MARK_END,
  ];
  return lines.join("\n");
}

function writeSources(rows) {
  const md = fs.readFileSync(SOURCES, "utf8");
  const block = sourcesBlock(rows);
  const s = md.indexOf(MARK_START), e = md.indexOf(MARK_END);
  const next = s >= 0 && e > s ? md.slice(0, s) + block + md.slice(e + MARK_END.length) : md.trimEnd() + "\n\n" + block + "\n";
  fs.writeFileSync(SOURCES, next, "utf8");
}

const shortStand = (s) => (s.match(/(\d{2}\.\d{2}\.\d{4})/) || [])[1] || s;

// ---------- Hauptprogramm ----------

async function list() {
  const cats = await getJson(`${base}/api/${lang}/systematic_categories`);
  const idx = await getJson(`${base}/api/${lang}/texts_of_law/lightweight_index`);
  const configured = new Set(CONFIG.documents.map((d) => d.nr));
  const walk = (c) => {
    const cat = c.systematic_category;
    console.log(`\n${cat.systematic_number} ${cat.name}`);
    for (const d of (idx[cat.id] || []).sort((a, b) => a.systematic_number.localeCompare(b.systematic_number, undefined, { numeric: true })))
      console.log(`  ${configured.has(d.systematic_number) ? "x" : " "} ${d.systematic_number.padEnd(8)} ${d.title}${d.abrogated ? " (aufgehoben)" : ""}`);
    cat.children.forEach(walk);
  };
  cats.forEach(walk);
  console.log("\nx = in tools/tlex-sources.json konfiguriert");
}

async function main() {
  const args = process.argv.slice(2);
  if (args.includes("--list")) return list();
  const check = args.includes("--check");
  const only = args.filter((a) => !a.startsWith("--"));
  const entries = CONFIG.documents.filter((d) => !only.length || only.includes(d.nr));
  if (only.length && entries.length !== only.length)
    throw new Error(`Nicht in tools/tlex-sources.json: ${only.filter((n) => !entries.some((e) => e.nr === n)).join(", ")}`);

  const today = new Date().toISOString().slice(0, 10);
  fs.mkdirSync(OUT_DIR, { recursive: true });
  const rows = [];
  let changed = 0;

  for (const entry of CONFIG.documents) {
    const old = existingFile(entry.nr);
    const oldHeader = old && readHeader(old);
    if (!entries.includes(entry)) {
      // nicht abgerufen: bestehende Angaben für sources.md übernehmen
      if (old) {
        const head = fs.readFileSync(old, "utf8").slice(0, 2000);
        const title = (head.match(/^Quelle: \S+ (.*)$/m) || [])[1] || entry.nr;
        const link = (head.match(/^Link: (.*)$/m) || [])[1] || "";
        rows.push({ ...entry, title, link, stand: shortStand(oldHeader.stand || ""), file: path.basename(old) });
      }
      continue;
    }
    let tol;
    try {
      tol = await fetchDoc(entry.nr);
    } catch (err) {
      console.log(`! ${entry.nr.padEnd(8)} Fehler: ${err.message}`);
      continue;
    }
    const sv = tol.selected_version;
    const isNew = !oldHeader || String(oldHeader.version) !== String(sv.id);
    const status = tol.abrogated ? "AUFGEHOBEN" : !oldHeader ? "neu" : isNew ? "NEUE FASSUNG" : "unverändert";
    if (isNew || tol.abrogated) changed++;
    console.log(`${isNew ? "*" : " "} ${entry.nr.padEnd(8)} ${status.padEnd(13)} ${shortStand(sv.version_dates_str).padEnd(11)} ${tol.title}`);

    const file = fileName(entry.nr, abbrOf(tol));
    rows.push({ ...entry, title: stripAbbr(tol.title) + (abbrOf(tol) ? ` (${abbrOf(tol)})` : ""), link: tol.canonical_link,
      stand: shortStand(sv.version_dates_str), file });
    if (check) continue;
    if (old && path.basename(old) !== file) fs.unlinkSync(old);
    fs.writeFileSync(path.join(OUT_DIR, file), toMarkdown(tol, entry, today), "utf8");
  }

  if (check) {
    console.log(changed ? `\n${changed} Erlass(e) neu oder geändert. Mit «node tools/fetch_tlex.mjs» aktualisieren.` : "\nAlles aktuell.");
    process.exitCode = changed ? 1 : 0;
    return;
  }
  rows.sort((a, b) => a.nr.localeCompare(b.nr, undefined, { numeric: true }));
  writeSources(rows);
  console.log(`\n${entries.length} Erlass(e) nach knowledge/fulltext/swissunihockey/ geschrieben, knowledge/sources.md nachgeführt.`);
}

main().catch((e) => { console.error(e.message); process.exit(2); });
