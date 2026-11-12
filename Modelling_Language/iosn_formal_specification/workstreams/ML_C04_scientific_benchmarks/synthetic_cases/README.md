# ML-C04 — synthetische Mikro-Referenzfälle

**Status:** SYNTHETIC_ONLY / NONNORMATIVE. Alle Zahlen einschließlich CY-Gewichten, Kosten, VoLL, Knotenflüssen, Verlustfaktoren, Effizienzen und Routenfaktor sind *frei erfundene, bewusst illustrative Prüfparameter*, niemals echte IoSN-Daten oder produktive Defaults. D2 bedeutet gemeinsame Gewicht**vektoren über Zieljahre**, nicht gleiche Gewichte unter den fünf CY.

- cases.json: 15 vollständig versionierte Eingangs- und Sollwerte, benannt B01–B15, jeweils mit einem vorgesehenen fachlichen Fehlermutanten.
- check_micro_oracles.py: reiner Python-Standardbibliothek-Selbsttest; prüft arithmetische und einige diskrete strukturelle Aussagen gegen festgehaltene Sollwerte. Aufruf: python3 check_micro_oracles.py [cases.json].
- Interpretation: PASS_SYNTHETIC belegt nur das interne Rechnen des jeweiligen Mini-Fall-Orakels; MUTANT_DETECTED zeigt nur, dass diese gezielte Mutation vom lokalen Prädikat unterschieden wird. Kein Toolmodell, Solver, Constraint-Generator, reale Quellendaten oder unabhängige Toolvalidierung wird dabei getestet.
- Die einzelnen positiven und adversarialen Formulierungen, Beweisgrenzen und SR/M-Referenzen stehen im scientific_benchmark_catalogue.md und analytical_reference_oracles.md. B06-Fixierung, B09-DSR-Shift, B15-Routenfaktor sind explizit *konditionale* Forschungsvarianten, keine beschlossene IoSN-Regel.
- Bei fehlender Methodikautorität oder KPI-/Discount-/Netz-Orakel: BLOCKED, nicht PASS. G1=BLOCKED.
