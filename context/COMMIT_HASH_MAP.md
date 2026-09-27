# Commit hash map (history rewrite, 2026-09-27)

On 2026-09-27 the history of every branch was rewritten to remove co-author trailers and to re-attribute one
commit. File contents did not change: every branch tip has the same tree as before, and the commit count of
every branch is unchanged. Only commit hashes changed. Documents written before the rewrite cite the OLD
hashes (for example `results/round3_final/ROUND3_REPORT.md`, `context/SESSION_HANDOFF_2026-09-27.md`,
`runs/fresh_run_2026-09-27/report/RUN_SUMMARY.md`); use this table to find the commit today. Commit messages
were rewritten to cite the new hashes. Tag `round3-final` now points to the new commit (old `27eb4f3`).

| Old | New | Date | Subject |
|---|---|---|---|
| `0a815a4` | `dcd0144` | 2026-09-26 | Add seasonal Gate 3b (monthly-CF re-ranking) with null models |
| `32e4a46` | `61fa7e4` | 2026-09-26 | Wire the legal-RAG corpus into L5 (cited evidence base) |
| `4b5325e` | `bd67a29` | 2026-09-26 | Update README |
| `76c1289` | `41f7d39` | 2026-09-26 | Complete the pipeline (L3-L9): forecast, routing, decisions, uncertainty, orchestrator |
| `782b4c3` | `af52054` | 2026-09-26 | Build L0-L2 account pipeline: facility spine to validated carbon+water account |
| `7d7729d` | `11fac8b` | 2026-09-26 | Fix headline numbers: state-month carbon, scope-1 ZLD, real routing oracle, siting grid |
| `7fb1ce0` | `0ab9c23` | 2026-09-26 | Initial commit: dcfootprint framework + research record |
| `d857d0a` | `1056ab7` | 2026-09-26 | Resolve review decisions: AWARE AMD budgets, split siting tables, triangular MC |
| `dc5127b` | `c41c514` | 2026-09-26 | Session 2026-09-26: architecture red-team + tiered contributions + first gate results |
| `071e689` | `22cb64b` | 2026-09-27 | Decision A: WUE upper bound 9 -> 2.5 L/kWh (MC band only) |
| `0a8ea57` | `5e7146f` | 2026-09-27 | Docs: rewrite READMEs for new readers (branch banner, start-here table, branch map, annotated file structure) |
| `0e14e7e` | `6a31b94` | 2026-09-27 | Add GADM 4.1 vs GEM state-label check (report only, no corrections) |
| `0f218ee` | `902ca3c` | 2026-09-27 | Add session handoff (2026-09-27): architecture as built, decisions, results, next actions |
| `118509d` | `a206f74` | 2026-09-27 | Docs: rewrite READMEs for new readers (branch banner, start-here table, branch map, annotated file structure) |
| `182f748` | `5813bd0` | 2026-09-27 | Plumbing: routing uses the pipeline's L4 incidence; levers take the in-memory account; drop dead account/water.py |
| `27eb4f3` | `e668000` | 2026-09-27 | Round 3 canonical run: snapshot, determinism, spot check, attribution report |
| `2931a40` | `b1d3b48` | 2026-09-27 | Forecasting run fresh_run_2026-09-27: all models scored with 10 metrics |
| `2b292c2` | `f96f5b4` | 2026-09-27 | Docs: rewrite READMEs for new readers (start-here table, quick start, branch map, annotated file structure) |
| `385ae2d` | `d574d6f` | 2026-09-27 | Q3: price decomposition as the routing solver (grid, basin, facility agents + coordinator) |
| `577c623` | `f09e528` | 2026-09-27 | L9: US and EU maps (Q1 siting rank, basin scarcity vs burden) |
| `5dae340` | `a03241d` | 2026-09-27 | Validation: pydantic config + pandera contracts at every layer boundary |
| `606f643` | `c06937d` | 2026-09-27 | Q1: 2030/2050 water scenarios (Aqueduct 4.0 0-5 scores) in minimax regret |
| `6554a55` | `98e71ae` | 2026-09-27 | pyproject: remove duplicate dev extra (pytest already in the existing dev extra) |
| `6c2e481` | `9e2eff6` | 2026-09-27 | Docs: rewrite READMEs for new readers (branch banner, start-here table, branch map, annotated file structure) |
| `9d61f4d` | `edbe93a` | 2026-09-27 | L9: paper figures (viz/figures.py) as a pipeline stage |
| `a985aa9` | `8a812ef` | 2026-09-27 | Docs: rewrite READMEs for new readers (branch banner, start-here table, branch map, annotated file structure) |
| `aacd856` | `d192477` | 2026-09-27 | L3 -> Q3: pre-registered one-step CI forecast (bottom-up SARIMA) feeds the routing controllers |
| `ba28e74` | `f3443c1` | 2026-09-27 | Decision B: document hyperscale cloud-region exclusion (no number changes) |
| `f0858fe` | `8bf3154` | 2026-09-27 | US + EU regions: region-aware inputs, US facility spine, EU country account, region runner |
| `f4863ac` | `64060a3` | 2026-09-27 | Docs: rewrite READMEs for new readers (branch banner, start-here table, branch map, annotated file structure) |
| `f56d765` | `2b7b797` | 2026-09-27 | L3: port SARIMA validity checks into hierarchy.py (fixes the US MinT blow-up) |
| `f80ff05` | `5b3e3b0` | 2026-09-27 | Decision C: GADM 4.1 state of record for GEM plants; drop >=2-plants rule |
