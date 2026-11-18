# ML-C17 — Adversarial Critical Language Review

**Unabhängigkeitsgrenze:** Separat durchgeführter KI-interner kritischer Review; **kein** personell unabhängiger wissenschaftlicher Audit und kein Domain-/Methodology-Owner-Signoff. Alle Gegenargumente gelten unabhängig von der Bewertung und vor jeder Architekturentscheidung.

## 1. Zwölf vorgegebene Fehlannahmen: Gegenbeispiele

| Nr. | Zu widerlegende Fehlannahme | Gegenbeispiel / falsifizierende Beobachtung | Ursache |
|---|---|---|---|
| 1 | Viele Knoten → hohe Reife | 528 Instanzen sind keine 528 Sprachbegriffe; 15 NODE-Typen teils noch ohne mathematisches AST | LANGUAGE_DESIGN |
| 2 | 48 SR-IDs → vollständige Ausdruckskraft | SR-045 Filter oder SR-032 Stage-Übergabe mit ungeklärtem Oracle | LANGUAGE_DESIGN+OWNER_TBD |
| 3 | gültiges JSON Schema → eindeutiges Mathemodell | M01 before-CY und M05 KVL können als freie Strings typvalidiert sein | LANGUAGE_DESIGN |
| 4 | gleiche synthetische Ergebnisse → gleiche Spracheignung | C06 alle 45/45 auf gemeinsamem Kernel; native Semantik nicht separat getestet | MISSING_EXPERIMENTAL_EVIDENCE |
| 5 | besonders ausdrucksstark = besonders einfach | mehr Klassen, Views und Profile können Lernlast erhöhen, ohne zusätzlichen wissenschaftlichen Sinn | LANGUAGE_DESIGN |
| 6 | Standard etabliert = für IoSN vollständig geeignet | ReqIF SR-Transport ist kein vollständiger Constraint-/Projection-Operatorbeweis | STANDARD_MAPPING_EVIDENCE |
| 7 | Spezifikation muss Optimierungscode erzeugen | gleiches contract-relevantes KVL als angle-/cycle-/PTDF-Implementierung | WRONG_SCOPE |
| 8 | alle Toolvariablen vorgeben | gleiche Entscheidungssemantik bei shared x vs gekoppelt repliziertem x | TOOLSPECIFIC_FREEDOM |
| 9 | Owner-TBD ist immer Sprachdefekt | F_y unbekannt, aber als Unknown(owner,specific_requirement,blocking_policy) präzise darstellbar | OWNER_TBD |
| 10 | Toolfunktion fehlt → Contract unbrauchbar | fehlende native Formulierung erfordert Adapter oder UNSUPPORTED statt Contractverlust | TOOL_LIMITATION |
| 11 | unterschiedliche Algebra = unterschiedliche Konformität | zwei zulässige optimalen Portfolios trotz unterschiedlicher Vektoren und Projektion | MATH_EQUIVALENCE |
| 12 | Strukturtests → produktive Sprachreife | 20 Graph-/CSV-Checks und 26 Boolean-Toys sind weder native Validatoren noch unabhängiger Review | MISSING_EVIDENCE |

## 2. Zusätzliche materialitätsbezogene Gegenprüfung

**CR01 — Zahlenspiel, HIGH:** Die realen C02-Forschungsinstanzen enthalten 528 Knoten/1323 Kanten, aber nur 15 tatsächlich materialisierte Knotentypen und 14 Relationsprädikate. Gleichzeitig fehlen vollständige materialisierte mathematische Expression-Typen, echte DataInstance-/TransformExecution- und Evidence-Objekte. Behauptungen „überkomplex“ wie „vollständig“ müssen erst mittels semantisch verlustfreier Ablation überprüft werden. Eine kleinere Graphdatei ist kein ausreichendes Ergebnis.

**CR02 — D2-Testfehler, HIGH:** Eine erste lokale ML-C17-Mikroregel behandelte nichtuniforme CY-Werte versehentlich als verpflichtend, statt lediglich als **zulässig**. Das war eine unzulässige zusätzliche fachliche Annahme. Korrigierte Tests akzeptieren ausdrücklich sowohl einen Uniformvektor [0.2,0.2,0.2,0.2,0.2] als auch einen Nichtuniformvektor [0.1,0.15,0.2,0.25,0.3], wenn er für identische CY über alle drei Studienjahre geteilt wird. Die tatsächlichen numerischen Werte sind weiterhin Owner-TBD; diese synthetischen Beispiele sind **keine** Festlegung.

**CR03 — eigener CSV-Parserdefekt, HIGH:** Beim ersten strukturellen Prüfversuch wurde ein Akkumulator beim Zeilenabschluss nicht zurückgesetzt; daraus entstanden acht Scheinausfälle. Der Fehler war im Prüfer, nicht in den Forschungsdaten. Korrigierte Lese-/Prüffassung lieferte 20/20 strukturierte PASS. Auch ein selbst korrigierter Checker ist noch keine externe unabhängige Validierung.

**CR04 — Ordinalbewertung als vermeintliche Metrik, HIGH:** 30 K1–K10-Konzeptscores A/B/C beruhen auf designbezogenen, nicht nutzergemessenen Urteilen. 36 RC-Rangpunkte sind NOT_EVALUATED. Das arithmetische Mittel oder eine Scheingewichtung wäre unzulässig; K2/K3/K6/K7 müssen als nicht kompensierbare Gates behandelt werden. Die realen Wartungs-/Lernkosten sind nicht gemessen.

**CR05 — semantisches FULL nicht positiv gezeigt, HIGH:** Die 48 Requirements sind referenziell nachgewiesen, aber die Fähigkeit der Sprache, *jeden vollständigen* Sachverhalt als formal typisierte überprüfbare Pflicht ausdrücken zu können, ist **INSUFFICIENT_EVIDENCE**. Das beweist nicht Unausdrückbarkeit; es verhindert einen unzulässigen Coverage-Fortschrittsprozentsatz.

**CR06 — die standardisierte Austauschform ist nicht der wissenschaftliche Beweis, HIGH:** ReqIF-, LinkML-, SysML-, SHACL- oder mathematische GEMS-Views können Teilinformationen transportieren. Eine verlustfreie Source-ID-Mappingrunde sagt nichts über E-FEAS/E-OPT/E-OBS mathematische Verträglichkeit oder native Unabhängigkeit. Ohne echten Parser und semantischen Roundtrip ist C noch kein gemessener Sieger.

**CR07 — Implementierungsfreiheit und Quellenstatus, HIGH:** Ein Tool könnte in einer Version keine direkte native OPF-/H2-/Stage-Implementierung besitzen, ohne dass der Requirements Contract unklar ist. Umgekehrt kann das erfolgreiche Lösen eines LP nicht nachweisen, dass die zugrunde liegende Source-authority und D2 korrekt interpretiert wurden.

**CR08 — Reduktionsrisiko, HIGH:** S1 ist für M01–M18 allein zu schwach. Ein als plausibel bezeichneter S2-Kern ist weder minimalitätsbewiesen noch syntaktisch vollständig. Aus S2 dürfen Unbekanntes/Ownerstatus, physikalische Branch-vs-Market-Link-Rolle, Unit/Index, Evidence und Version nicht wegoptimiert werden, auch wenn die Entitätszahl sinkt.

## 3. Gegenüberstellung der verbleibenden Unsicherheiten

| Kategorie | Noch offenes Thema | Konsequenz |
|---|---|---|
| Sprache | Quantoren/AST, mathematical projection, carrier/asset/state/guard, Output/Proofstatus, semantic revision | neue Sprachentwicklung, kein Ownerentscheid |
| Fachmethodik | MD-01, MD-07, MD-12, H2-Basis, KPI-D081, N-1-Oracle, 21 MD/CL | Owner-TBD beibehalten, nicht durch Syntax ersetzen |
| Data Governance | echte Originaldaten, Release-/Provenienz-/Approval-Status | späteres Gate, nicht ML-C17-Prüfgegenstand |
| Experiment | native Parser, 48 formalisiert, RC-Mutanten, zwei unabhängige Implementer, E04 toy rows | L3/L4-Sprachbeleg fehlt |
| Toolspezifisch | tatsächliche Capability/Adapter jedes Version-Paarings | gesondertes Implementer-Handover, kein allgemeiner Sprachmangel |

## 4. Adversarielles Abschlussurteil

**Research-only konditionale Präferenz:** Ein semantisch vollständiger S2-Kern ist ein vertretbarer kleinster **zu erforschender** Contract-Zustand, solange seine Vollständigkeit und Minimalität explizit falsifizierbar bleiben. Daraus folgt **keine** Entscheidung für die integrierte Architektur B; A, B und C können alle denselben Kern tragen. Kein externer Review, kein nativ geprüfter Parser und keine wissenschaftliche Toolzertifizierung.

**CRITICAL_REVIEW_STATUS = AI_INTERNAL_ONLY; ADR_DEFERRED; G1_BLOCKED.**
