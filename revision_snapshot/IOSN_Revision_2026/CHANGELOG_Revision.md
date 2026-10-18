# IoSN/TYNDP2026: Revision des wissenschaftlichen Berichtspakets

**Stand:** 16. Oktober 2026. Die wissenschaftliche Baseline ist die
ENTSO-E IoSN-Methodik (Konsultationsfassung 25.02.2026, §§3.8–3.9, Annex 6.1).

## Maßgebliche Berichtsfassungen

1. **Band I:** Wissenschaftlicher Methodenvergleich und mathematische Theorie.
   Zwei Clustering-Methoden; exakte Aggregation; Technologie-PTDF;
   Merit-Order-Referenzen; Ersatzknoten; Ersatzimpedanz und strukturelles F0;
   IoSN-nahe, analytische und konservative N-1-Kapazitäten;
   Woodbury und duale Kreisfluss-LODFs; FBMC.
2. **Band II:** PyPSA-Softwaredesign, Daten-/Quellenverträge,
   Validierungs- und Qualitätsgates, bekannte Einschränkungen und
   reproduzierbarer Python-Prototyp.

Jeder Methodenblock ist als **IoSN-dokumentiert**, **rekonstruiert**,
**wissenschaftliche Erweiterung** oder **nur synthetisch geprüft** eingeordnet.
Frühere Einzelberichte werden durch diese konsolidierten Bände ersetzt.

## Numerische Prüfung

- 24 automatisierte Kernprüfungen mit NumPy/SciPy/Pandas bestanden.
- Synthetischer Neunknotenvergleich reproduziert (A/B, drei Referenzverteilungen).
- Primal/duale LODF auf Dreieck und vermaschtem Netz abgeglichen.
- Woodbury-Rang-eins-Update gegen direkte Inversion abgeglichen.
- N-1-sicherer A→B-Inkrementtransfer im Dreieck: 80 MW (N-0: 150 MW).
- Vorhandener FBMC-Demonstrator auf synthetischen 9-Knoten-Daten erneut ausgeführt.
- **Nicht geprüft:** reale PyPSA-Laufzeitintegration, echte ENTSO-E-/TYNDP-Daten,
  operative Core/JAO-FBMC-Kapazitätsberechnung, vollständige Gerätesemantik.

## Fachliche Klarstellungen gegenüber älteren Fassungen

- `R_k` ändert nicht die physikalische nodale PTDF, sondern die räumliche
  Verteilung der zonalen Einspeisung.
- Ein struktureller zeitvariabler Fluss ist nicht identisch mit einem
  szenarioweise kalibrierten konstanten `F0`.
- `A_z Gamma = P A_d` beweist die Bilanz, nicht das Ohm-/KVL-Äquivalent.
- Die bilaterale Transfergrenze ist keine allgemeine Ersatzleitungsgrenze.
- K1 (IoSN-nahe stündliche Kapazität) ist vom LODF/CNEC-Polyeder K2 und von
  der konservativen Derating-Approximation K3 zu unterscheiden.
- Die relevante ENTSO-E-Quelle beschreibt nicht die operativen RAMs von Core FBMC.

## Quellen

ENTSO-E IoSN 2026: https://eepublicdownloads.blob.core.windows.net/public-cdn-container/clean-documents/tyndp-documents/TYNDP2026/TYNDP_2026_identification_of_system_needs_methodology_for_consultation.pdf
