# ML-C20/04 – Formal candidate grammars, type system and error rules
ML-C20 research-r0.1 | 2026-11-23 | NON-NORMATIVE / RESEARCH ONLY
B0 CSNF commit: 2f0297b754e3a96a2523a34d3af98782b26181f3; ML-C18 SLR01–42 / K01–17; ML-C19 C1–C9, R00–R13, E1–E5. H0 SysML/KerML is evaluated independently in C22. G1 BLOCKED.

## Candidate A: Compact Study Contract Notation (C-SCN), restricted EBNF research-r0.1
```ebnf
Contract      ::= "contract" QID "schema" STRING "rules" STRING "registry" STRING "{" Decl* "}" ;
Decl          ::= Frame | Referent | Relation | Predicate | Assertion | Observable | Variation | Evidence | Authority ;
Frame         ::= "frame" QID "{" Field* "}" ;
Referent      ::= "referent" QID ":" IDENT "{" Field* "}" ;
Relation      ::= "relation" QID ":" IDENT "(" QID "," QID ")" "{" Field* "}" ;
Predicate     ::= "predicate" QID "=" Expr ";" ;
Assertion     ::= "assert" QID Modality SemanticRole "predicate" QID "scope" QID "guard" Expr
                  "authority" "[" QID ("," QID)* "]" "decision" Decision ";" ;
Observable    ::= "observe" QID "from" QID "{" Field* "}" ;
Variation     ::= "variation" QID "on" QID "{" Field* "}" ;
Evidence      ::= "evidence" QID ":" ("REQUEST" | "RESULT") "for" QID "{" Field* "}" ;
Authority     ::= "authority" QID ":" ("SOURCE" | "OWNER" | "DECISION" | "PROVENANCE") "{" Field* "}" ;
Field         ::= IDENT ":" Value ";" ;
Value         ::= STRING | NUMBER | IDENT | QID | "[" [Value ("," Value)*] "]" | "{" Field* "}" ;
Expr          ::= Call | QID | NUMBER | "true" | "false" | "unknown" | "not" "(" Expr ")" ;
Call          ::= IDENT "(" [Expr ("," Expr)*] ")" ;
Modality      ::= "REQUIRED" | "PROHIBITED" | "PERMITTED" | "IMPLEMENTATION_DEFINED" | "CONDITIONAL" ;
SemanticRole  ::= "ENVIRONMENT_ASSUMPTION" | "DATA_ASSUMPTION" | "TECHNICAL_ASSUMPTION"
                | "SAFETY_GUARANTEE" | "SERVICE_GUARANTEE" | "CAPABILITY_GUARANTEE" ;
Decision      ::= "APPROVED" | "PROPOSED" | "OWNER_TBD" | "REJECTED" | "SUPERSEDED" | "UNKNOWN" ;
QID           ::= STRING ;  (* UTF-8 URI/URN string with namespace and stable identity; alias resolved separately *)
```
No hidden infix precedence; explicit typed Call AST (`and`, `or`, `not`, `eq`, `le`, `gte`, `forall`, `exists`, `quantity`, `trace`, `hasInformationAt`, `portCompatible`, `inScope`, `aggregate`, `ledger`). Arity and operator signatures are resolved by typed registry, so EBNF syntax acceptance alone cannot prove type correctness. Extensible operator catalog requires version+authority; quantifier scope and `forall request exists response` order must be preserved.

## Candidate B: Structured typed document
A versioned JSON document with arrays for nine typed roles and discriminated unions. Formal wellformedness: JSON RFC 8259 parsing + JSON Schema 2020-12 (`schema/contract_document.schema.json` research subset) + semantic checks by same typed AST registry as Candidate A. JSON `null` is NOT equivalent to UNKNOWN; missing keys are diagnosed unless explicitly optional with source-backed default. JSON arrays are not necessarily sets: ordering behavior belongs to the field type, not the serializer. `additionalProperties:false` for versioned core objects; profile fields only in versioned profile registry.

## Type rules / static diagnostics
Γ⊢ref(id):T where namespace+kind unambiguous; Γ⊢port(p):Port(carrier,physical_kind,dim,unit,sign,direction) and Γ⊢connect(p,q):ok only if carrier/quantity/time/support and physical endpoint adapter explicitly agree. Γ⊢sum(quantity(T),quantity(T)):Quantity(T) only if basis and sign unified. Γ⊢compare(q1,q2):Bool3 only if same compatible measurement; duration × power yields energy only for explicit integration support. Γ⊢and(Bool3,Bool3):Bool3; Guard must be Bool3. Quantifier domain and information set typed; service guarantees must not be replaced by a single `exists trace` witness. Errors carry code, AST path, source span, source-id, registry/rule version, expected/actual types, conservative verdict. Existence of a type rule does not establish global physical feasibility.
