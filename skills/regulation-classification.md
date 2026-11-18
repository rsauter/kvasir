# Skill: Reglemente einordnen

Verwenden, sobald eine Fundstelle gefunden ist und bevor du daraus eine Antwort ableitest.
Der Skill `regulation-research` ruft ihn auf. Der Agent `librarian` braucht ihn beim
Aufnehmen neuer Quellen.

## 1. Ebene bestimmen

| Ebene | Beispiele | Bindung |
|---|---|---|
| Bundesrecht | ZGB (Vereinsrecht, Art. 60 ff.), OR (Buchführung, Art. 957 ff.), Steuer- und Sozialversicherungsrecht | Zwingende Bestimmungen gehen allem anderen vor. |
| Kanton | Kantonales Recht (zum Beispiel Geldspielgesetz KGSG und -verordnung KGSV im Kanton Bern) und Praxisleitfäden der Verwaltung | Gesetz und Verordnung binden. Ein Praxisleitfaden zeigt, wie die Behörde entscheidet: für Gesuche massgebend, aber eine Auslegungshilfe, kein Gesetz. Beiträge sind keine Pflicht, sondern ein Angebot mit Bedingungen. |
| Swiss Olympic | Ethik-Charta und weitere Vorgaben | Bindet Swiss Unihockey und über die Mitgliedschaft den Verein. |
| Jugend+Sport | Bedingungen für Beiträge und Ausbildung | Bindet, wenn der Verein J+S-Angebote durchführt oder Beiträge bezieht. Das ist eine Voraussetzung, keine Mitgliedschaftspflicht. |
| Swiss Unihockey | Spielregeln, Wettbewerbs-, Lizenz-, Gebühren- und Rechtspflegereglemente | Bindet den Verein über die Mitgliedschaft. |
| Kantonalverband | Weisungen, Wettbewerbsbestimmungen, Gebühren | Bindet den Verein über die Mitgliedschaft. |
| Verein | Statuten, Reglemente, Beschlüsse von Vorstand und Hauptversammlung | Bindet die Mitglieder und Organe. Darf den Ebenen darüber nicht widersprechen. |
| Vertrag | Sponsoring-, Ausrüster- und Hallenmietverträge | Bindet nur die Vertragsparteien. |

## 2. Verbindlichkeit bestimmen

- **Pflicht:** Der Text verpflichtet («muss», «hat zu», «ist verpflichtet», «ist verboten»).
- **Empfehlung:** Der Text lässt Spielraum («soll», «kann», «wird empfohlen»).
- **Auslegungshilfe:** Merkblätter, FAQ, Präsentationen und Musterdokumente erklären ein
  Reglement, ersetzen es aber nicht.
- **Praxis:** Eine Gewohnheit, die nicht schriftlich geregelt ist. Als solche kennzeichnen.

## 3. Geltungsbereich prüfen

- Für welche Liga, Altersklasse und Kategorie gilt die Bestimmung? Gilt sie für Grossfeld,
  Kleinfeld oder beides?
- Ab wann und bis wann gilt sie? Gibt es Übergangsbestimmungen?
- Nennt dasselbe Dokument Ausnahmen oder Sonderfälle?
- Passt der Geltungsbereich nicht eindeutig zur Frage, frage nach (siehe `rules/01-core-rules.md`).

## 4. Aktualität prüfen

- Stand der Quelle aus `knowledge/sources.md` oder aus dem Kopf des Auszugs entnehmen.
- Ist die Quelle älter als ein Jahr oder ohne Stand, darauf hinweisen.
- Ausnahme automatisch geholte Volltexte (Swiss Unihockey aus TLex, kantonale Leitfäden): «in Kraft seit» ist das Datum der gültigen Fassung. Ein altes Datum heisst nicht veraltet. Massgebend für die Aktualität ist das Prüfdatum: der Stand des Pakets (Kopf von `kvasir.md` bzw. der Wissensdatei, dort wird vor jedem Paket auf neue Fassungen geprüft), sonst «Ausgezogen am». Ist es älter als drei Monate, empfehle ein neues Kvasir-Paket.
- Reglemente können sich auf eine neue Saison hin ändern. Bei Fragen zum Spielbetrieb
  prüfen, ob der Stand zur gefragten Saison passt.
- Ein Auszug ist eine Arbeitskopie. Für Entscheide gilt das Original.

## 5. Verhältnis zu anderen Fundstellen

- Die höhere Ebene geht der tieferen vor, ausser sie lässt ausdrücklich Spielraum.
- Auf derselben Ebene geht die spezielle Bestimmung der allgemeinen vor und die neuere der älteren.
- Widersprechen sich Fundstellen, melde den Widerspruch und entscheide nicht selbst
  (siehe `rules/01-core-rules.md`).

## Ergebnis

Eine Zeile pro Fundstelle, die in die Quellenangabe der Antwort übernommen wird:

```
[Ebene] Dokument, Art. X Abs. Y, Stand – Pflicht | Empfehlung | Auslegungshilfe | Praxis – gilt für … – Hinweis
```

Beispiel mit Platzhaltern:

```
[Swiss Unihockey] Wettbewerbsreglement, Art. … Abs. …, Stand … – Pflicht – gilt für Grossfeld, alle Ligen – Quelle älter als ein Jahr
```
