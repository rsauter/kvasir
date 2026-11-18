# Quellenliste

Hier stehen die Quellen, die Agenten verwenden dürfen.

Kvasir ist in Schichten aufgebaut:

| Schicht | Ordner | Inhalt | Wer pflegt |
|---|---|---|---|
| Kern | `fulltext/swissunihockey/` | Erlasse von Swiss Unihockey | Kvasir, automatisch aus TLex |
| Kanton | `fulltext/canton-<kürzel>/` | Kantonale Förderung, zum Beispiel Sport- und Lotteriefonds. Zurzeit vorhanden: Bern (`canton-be`) | Kvasir. Weitere Kantone kommen dazu, sobald jemand die Quellen nennt. |
| Verein | `club/` | Statuten, Reglemente, Konzepte des eigenen Vereins | Jeder Verein selbst |
| Auszüge | `excerpts/` | Ausgewählte Artikel, klein genug für Gratis-KIs | Agent `librarian` |

Dateien in `fulltext/` werden automatisch erzeugt. Nicht von Hand ändern.

## Übersicht

| Quelle | Thema | Link zum Dokument | Text vorhanden | Stand |
|---|---|---|---|---|
| Statuten und Reglemente des Vereins | Organisation, Zuständigkeiten, Finanzen | – | in `club/`, falls der Verein sie abgelegt hat | |
| Regional- bzw. Kantonalverband | Spielbetrieb, Nachwuchs, Gebühren | je nach Region | nein, noch nicht erfasst | |
| Swiss Unihockey | Alle Erlasse, siehe unten | https://swissunihockey.tlex.ch/app/de/systematic/texts_of_law | ja, `fulltext/swissunihockey/` | siehe unten |
| Kanton Bern: Sport- und Lotteriefonds | Beiträge an Vereine, Fristen | https://www.fobe.sid.be.ch/de/start/ueber-uns/rechtliche-grundlagen.html | ja, `fulltext/canton-be/` | siehe unten |
| Swiss Olympic: Ethik-Charta und Vorgaben | Ethik, Nachwuchs, Partner | swissolympic.ch (Dokument einsetzen) | nein | |
| Jugend+Sport | Beiträge, Ausbildung | jugendundsport.ch (Dokument einsetzen) | nein | |
| ZGB, Vereinsrecht (Art. 60 ff.) | Vereine | fedlex.admin.ch | nein | |
| OR, Buchführung (Art. 957 ff.) | Finanzen | fedlex.admin.ch | nein | |

## Swiss Unihockey (TLex)

Swiss Unihockey führt alle Erlasse in TLex, immer in der gültigen Fassung. Die Liste und die
Volltexte erzeugt `node tools/fetch_tlex.mjs`. Welche Erlasse dazugehören, steht in
`tools/tlex-sources.json`. Bereich «kern» betrifft die meisten Vereine (Regionalliga),
«ergänzend» zum Beispiel die Nationalliga oder Senioren.

<!-- tlex:start -->
<!-- Dieser Block wird von tools/fetch_tlex.mjs erzeugt. Nicht von Hand ändern. -->

Systematik: https://swissunihockey.tlex.ch/app/de/systematic/texts_of_law

| Nr. | Erlass | Bereich | Relevant für | Stand | Volltext |
|---|---|---|---|---|---|
| 1-1 | [Statuten](https://swissunihockey.tlex.ch/app/de/texts_of_law/1-1) | kern | president | 23.11.2024 | `fulltext/swissunihockey/swissunihockey-1-1.md` |
| 2-1 | [Tarif-, Gebühren-, Bussen-Reglement (TGB)](https://swissunihockey.tlex.ch/app/de/texts_of_law/2-1) | kern | treasurer, match-operations | 01.05.2026 | `fulltext/swissunihockey/swissunihockey-2-1-tgb.md` |
| 2-3 | [Funktionärsreglement Entschädigungen](https://swissunihockey.tlex.ch/app/de/texts_of_law/2-3) | ergänzend | treasurer | 01.05.2026 | `fulltext/swissunihockey/swissunihockey-2-3.md` |
| 2-4 | [Werbereglement (WER)](https://swissunihockey.tlex.ch/app/de/texts_of_law/2-4) | kern | sponsorship | 03.05.2016 | `fulltext/swissunihockey/swissunihockey-2-4-wer.md` |
| 3-1 | [Wettspielreglement (WSR)](https://swissunihockey.tlex.ch/app/de/texts_of_law/3-1) | kern | match-operations, president | 10.06.2026 | `fulltext/swissunihockey/swissunihockey-3-1-wsr.md` |
| 3-2 | [Wettspiel-Reglement Cup (WSC)](https://swissunihockey.tlex.ch/app/de/texts_of_law/3-2) | kern | match-operations | 01.09.2026 | `fulltext/swissunihockey/swissunihockey-3-2-wsc.md` |
| 3-3 | [Weisung Cupwettbewerbe (WSCW1)](https://swissunihockey.tlex.ch/app/de/texts_of_law/3-3) | kern | match-operations | 01.09.2026 | `fulltext/swissunihockey/swissunihockey-3-3-wscw1.md` |
| 3-4 | [Spielregeln (SPR)](https://swissunihockey.tlex.ch/app/de/texts_of_law/3-4) | kern | match-operations, youth | 01.11.2026 | `fulltext/swissunihockey/swissunihockey-3-4-spr.md` |
| 3-5 | [Weisung Spieldurchführung](https://swissunihockey.tlex.ch/app/de/texts_of_law/3-5) | kern | match-operations | 01.09.2026 | `fulltext/swissunihockey/swissunihockey-3-5.md` |
| 3-6 | [Weisung Senioren-Meisterschaft](https://swissunihockey.tlex.ch/app/de/texts_of_law/3-6) | ergänzend | match-operations | 01.05.2021 | `fulltext/swissunihockey/swissunihockey-3-6.md` |
| 3-7 | [Weisung und Spielregeln Junior/-innen D (WJD)](https://swissunihockey.tlex.ch/app/de/texts_of_law/3-7) | kern | youth, match-operations | 01.10.2026 | `fulltext/swissunihockey/swissunihockey-3-7-wjd.md` |
| 3-8 | [Weisung und Spielregeln Junior/-innen E (WJE)](https://swissunihockey.tlex.ch/app/de/texts_of_law/3-8) | kern | youth, match-operations | 01.10.2026 | `fulltext/swissunihockey/swissunihockey-3-8-wje.md` |
| 3-9 | [Spielsekretärenreglement (SPS)](https://swissunihockey.tlex.ch/app/de/texts_of_law/3-9) | kern | match-operations | 01.09.2026 | `fulltext/swissunihockey/swissunihockey-3-9-sps.md` |
| 3-10 | [Lizenzreglement (LZR)](https://swissunihockey.tlex.ch/app/de/texts_of_law/3-10) | kern | match-operations, youth, treasurer | 27.08.2008 | `fulltext/swissunihockey/swissunihockey-3-10-lzr.md` |
| 3-11 | [Weisung Lizenzierung & Spielerqualifikation](https://swissunihockey.tlex.ch/app/de/texts_of_law/3-11) | kern | match-operations, youth | 01.05.2026 | `fulltext/swissunihockey/swissunihockey-3-11.md` |
| 3-12 | [Online Game Report Reglement (OGR)](https://swissunihockey.tlex.ch/app/de/texts_of_law/3-12) | kern | match-operations | 01.05.2026 | `fulltext/swissunihockey/swissunihockey-3-12-ogr.md` |
| 3-13 | [Weisung Nachträglicher Videoentscheid (SPAW12)](https://swissunihockey.tlex.ch/app/de/texts_of_law/3-13) | ergänzend | match-operations | 01.08.2026 | `fulltext/swissunihockey/swissunihockey-3-13-spaw12.md` |
| 4-1 | [Schiedsrichterreglement (SRR)](https://swissunihockey.tlex.ch/app/de/texts_of_law/4-1) | kern | match-operations, president | 01.05.2026 | `fulltext/swissunihockey/swissunihockey-4-1-srr.md` |
| 4-2 | [Schiedsrichterfonds Reglement (SRF)](https://swissunihockey.tlex.ch/app/de/texts_of_law/4-2) | kern | treasurer, match-operations | 01.05.2021 | `fulltext/swissunihockey/swissunihockey-4-2-srf.md` |
| 5.1-1 | [Nationalliga-Reglement (NLR)](https://swissunihockey.tlex.ch/app/de/texts_of_law/5.1-1) | ergänzend | president, match-operations | 20.06.2026 | `fulltext/swissunihockey/swissunihockey-5_1-1-nlr.md` |
| 5.1-2 | [Weisung Anwesenheit Sitzungen](https://swissunihockey.tlex.ch/app/de/texts_of_law/5.1-2) | ergänzend | president | 13.05.2019 | `fulltext/swissunihockey/swissunihockey-5_1-2.md` |
| 5.1-4 | [Weisung Video-Spielaufzeichnung NLA Frauen und NLA Männer](https://swissunihockey.tlex.ch/app/de/texts_of_law/5.1-4) | ergänzend | match-operations | 01.09.2021 | `fulltext/swissunihockey/swissunihockey-5_1-4.md` |
| 5.1-5 | [Weisung Nationalliga Fonds](https://swissunihockey.tlex.ch/app/de/texts_of_law/5.1-5) | ergänzend | treasurer | 15.11.2018 | `fulltext/swissunihockey/swissunihockey-5_1-5.md` |
| 5.1-6 | [Weisung Auftritt NL - Erscheinungsbild](https://swissunihockey.tlex.ch/app/de/texts_of_law/5.1-6) | ergänzend | sponsorship | 22.06.2020 | `fulltext/swissunihockey/swissunihockey-5_1-6.md` |
| 5.1-8 | [Weisung Topscorer Scoringliste](https://swissunihockey.tlex.ch/app/de/texts_of_law/5.1-8) | ergänzend | match-operations | 01.09.2015 | `fulltext/swissunihockey/swissunihockey-5_1-8.md` |
| 5.1-9 | [Weisung Unterstützung Eventspiel](https://swissunihockey.tlex.ch/app/de/texts_of_law/5.1-9) | ergänzend | sponsorship, treasurer | 03.05.2019 | `fulltext/swissunihockey/swissunihockey-5_1-9.md` |
| 5.1-10 | [Weisung Supercup](https://swissunihockey.tlex.ch/app/de/texts_of_law/5.1-10) | ergänzend | match-operations | 17.10.2022 | `fulltext/swissunihockey/swissunihockey-5_1-10.md` |
| 5.1-11 | [Erfassung Verletzungen NLA](https://swissunihockey.tlex.ch/app/de/texts_of_law/5.1-11) | ergänzend | match-operations | 01.08.2022 | `fulltext/swissunihockey/swissunihockey-5_1-11.md` |
| 5.1-12 | [Vorgaben Spielfläche L-UPL (NLR)](https://swissunihockey.tlex.ch/app/de/texts_of_law/5.1-12) | ergänzend | match-operations | 01.09.2025 | `fulltext/swissunihockey/swissunihockey-5_1-12-nlr.md` |
| 5.2-1 | [Regionalliga-Reglement (RLR)](https://swissunihockey.tlex.ch/app/de/texts_of_law/5.2-1) | kern | president, match-operations, treasurer | 23.06.2026 | `fulltext/swissunihockey/swissunihockey-5_2-1-rlr.md` |
| 5.2-11 | [Weisung Gewährleistung Statuten Mitgliedsverbände Regionalliga (WGSMR)](https://swissunihockey.tlex.ch/app/de/texts_of_law/5.2-11) | kern | president | 13.01.2025 | `fulltext/swissunihockey/swissunihockey-5_2-11-wgsmr.md` |
| 5.2-12 | [Weisung Regionalligafonds (WRLF)](https://swissunihockey.tlex.ch/app/de/texts_of_law/5.2-12) | kern | treasurer | 01.01.2025 | `fulltext/swissunihockey/swissunihockey-5_2-12-wrlf.md` |
| 6-1 | [Rechtspflegereglement (RPR)](https://swissunihockey.tlex.ch/app/de/texts_of_law/6-1) | kern | match-operations, president | 06.11.2022 | `fulltext/swissunihockey/swissunihockey-6-1-rpr.md` |

<!-- tlex:end -->

## Kanton Bern: Lotterie- und Sportfonds (Modul `canton-be`)

Gilt nur für Vereine mit Sitz im Kanton Bern. Andere Kantone haben eigene Fonds mit eigenen Regeln.

Die Praxisleitfäden des Kantons Bern (Fonds und Bewilligungen, Sicherheitsdirektion) legen fest, wofür
Vereine Beiträge aus dem Sport- und dem Lotteriefonds erhalten, mit Fristen und Beträgen. Sie
konkretisieren das kantonale Geldspielgesetz (KGSG) und die Geldspielverordnung (KGSV).
Übersicht: https://www.fobe.sid.be.ch/de/start/ueber-uns/rechtliche-grundlagen.html

Volltexte und Tabelle erzeugt `python tools/fetch_pdfs.py`, die Liste steht in `tools/pdf-sources.json`.

<!-- pdf:start -->
<!-- Dieser Block wird von tools/fetch_pdfs.py erzeugt. Nicht von Hand ändern. -->

| Modul | Dokument | Herausgeber | Bereich | Relevant für | Stand | Volltext |
|---|---|---|---|---|---|---|
| canton-be | [Praxisleitfaden Sportfonds](https://www.fobe.sid.be.ch/content/dam/fobe_sid/dokumente/de/sportfonds/2026%20Praxisleitfaden%20Sportfonds.pdf) | Kanton Bern, Sicherheitsdirektion, Fonds und Bewilligungen (FOBE) | kern | treasurer, youth, president, match-operations | 05/2026 | `fulltext/canton-be/be-sportfonds-praxisleitfaden.md` |
| canton-be | [Praxisleitfaden Lotteriefonds](https://www.fobe.sid.be.ch/content/dam/fobe_sid/dokumente/de/%C3%BCber-uns/2026%20Praxisleitfaden%20Lotteriefonds.pdf) | Kanton Bern, Sicherheitsdirektion, Fonds und Bewilligungen (FOBE) | ergänzend | president, treasurer, sponsorship | 05/2026 | `fulltext/canton-be/be-lotteriefonds-praxisleitfaden.md` |

<!-- pdf:end -->
