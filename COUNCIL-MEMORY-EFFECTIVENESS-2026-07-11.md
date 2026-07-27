# Council Report: RecursiveIntell Memory System Effectiveness

**Date**: 2026-07-11 (session live probes through 2026-07-12T01:15Z)  
**Mode**: Multi-lane council + controller reconciliation (read-only)  
**Subject**: Grok Build dual-rail semantic-memory stack (shared with Hermes / Claude / Codex)  
**Status**: Complete

---

## Council composition

| Lane | Role | Overall |
|------|------|--------:|
| **1** Architecture / Runtime | Store unity, process topology, binary/schema, dual-rail, companions | **4.8 / 10** |
| **2** Retrieval / Content Quality | Recall relevance, freshness, noise, graph, receipts | **5.0 / 10** |
| **3** Governance / Safety / Adversarial | Privilege, injection, capture, admin reliability, auditability | **5.2 / 10** |
| **Controller** (this report) | Live re-probes; resolve conflicts; final claim | **5.0 / 10** |

Method follows the context-compactor council pattern: independent lanes report; controller re-inspects source and owns final claims.

---

## Executive verdict

**Overall effectiveness: 5.0 / 10 — usable continuity accelerator, not yet a high-trust shared SoR.**

The *design* of the new Grok dual-rail stack is strong: agent profile (16 tools) + admin full, warm HTTP owned by systemd (1739 coding / 1738 Hermes), markdown memory off, witnessed search with receipts, companions (context-governor, claim-ledger), and coherent AGENTS playbooks across hosts.

Live effectiveness is pulled down by three structural facts:

1. **Single store is policy-true and practice-false** — Hermes MCP still points at `~/.local/share/semantic-memory` while Grok/hooks/systemd use `~/.hermes/semantic-memory.db`.
2. **Integrity is red** — schema **36** is ahead of what warm HTTP reports as supported (**34**); 16 facts missing embeddings; pending HNSW ops; embedding_metadata dirty flag set.
3. **Stale “CURRENT STATE” infrastructure facts still rank** for broad system queries unless the query is specific enough to surface the 2026-07-11 Grok dual-rail facts.

For cooperative coding with human oversight and **live file verification**, the system helps. As a high-assurance multi-agent knowledge SoR, it is **not promotion-ready**.

---

## Live baseline (controller-verified)

| Signal | Value |
|--------|------:|
| Canonical store | `/home/sikmindz/.hermes/semantic-memory.db` (19MB, SQLite OK, WAL) |
| Legacy store | `/home/sikmindz/.local/share/semantic-memory` (**314** facts, still live) |
| Facts / edges / chunks / docs | **657** / **954** / **473** / **20** |
| Messages / sessions | **139** / **3** |
| Namespaces | **24** (incl. hostile-* fixtures) |
| Embedder | nomic-embed-text-v1.5 · 768d · Candle |
| Graph component health (MCP stats) | core + graph report healthy |
| HTTP `/health` 1738 & 1739 | OK |
| HTTP `/verify-integrity` | **integrity: false** (5 issues) |
| Schema version in DB | **36** |
| Grok agent MCP | hermes dir · agent · 16 tools · works |
| Grok admin MCP | hermes dir · full · flaky handshake at session start |
| Context-governor receipts | **123+** under `~/.local/share/context-governor/receipts` (+ Hermes silo) |
| Claim-ledger host root | not materialized as default path |

### Integrity issues (both warm ports)

1. schema version 36 is ahead of supported 34  
2. 16 facts missing embeddings  
3. 2 pending HNSW sidecar delete ops  

### Dual-store smoking gun

`~/.hermes/config.yaml`:

```yaml
mcp_servers:
  semantic_memory:
    args:
      - --memory-dir
      - /home/sikmindz/.local/share/semantic-memory   # diverges from AGENTS SoR
      - --tool-profile
      - agent
```

Hermes **hooks** still set `SEMANTIC_MEMORY_DIR=.../.hermes/semantic-memory.db` and HTTP 1738 → read/write split-brain.

---

## Dimension scorecard (reconciled)

| Dimension | Score | Controller note |
|-----------|------:|-----------------|
| Store unity / single SoR | **3.5** | Hermes MCP regression is decisive |
| Process topology | **6.0** | Systemd dual warm ports + Grok HTTP_PORT=0 are good; multi-writer remains |
| Schema / binary compatibility | **2.5** | Integrity permanently false until binary catches schema 36 |
| Dual-rail design (agent/admin) | **8.5** | Best part of Grok config |
| Dual-rail enforcement (live) | **4.5** | Admin always-on + `permission_mode=always-approve` |
| Companion stack | **5.5** | Governor active; ledger tools exist but not host-defaulted; CG silos |
| Cross-agent sharing | **4.5** | Paper aligned; Hermes MCP breaks share |
| Recall relevance | **6.5** | Specific queries hit right durable facts (Grok dual-rail CURRENT STATE ranks #1 when query names it) |
| Freshness / staleness control | **3.5** | Generic “system effectiveness” still surfaces June status heads |
| Noise / junk | **5.5** | Controller correction: ASYNC DELEGATION / Memory-updated **0** today; residual is fragment capture in `general` + stale status |
| Conversation memory | **4.5** | Works; only 3 sessions / 139 messages |
| Graph utility | **4.0** | Edges exist; weak for discovery |
| Receipt / provenance | **7.5** | Witnessed receipts excellent; trust still `persisted_unjudged` |
| Injection / hostile resistance | **5.5** | Framing design good; denylist wildcard concerns; soft containment |
| Capture hygiene (enforcement) | **4.0** | Prose gates strong; server gates weak; multi-host writers |
| Admin reliability | **5.0** | Works under load sometimes; Broken-pipe class failures observed |

---

## What works well (do not regress)

1. **Grok dual-rail config is the reference implementation** on this host: agent vs full, stdio `HTTP_PORT=0`, cargo binary pin, markdown memory off.
2. **Systemd warm HTTP ownership** (1738 Hermes / 1739 coding) is sound and running.
3. **AGENTS cold-start / escalate / capture / high-stakes** playbook is coherent across Grok and Claude.
4. **`sm_search_witnessed`** returns real receipts (request_id, digests, epochs, stage outcomes).
5. **Targeted infrastructure queries** surface the 2026-07-11 dual-rail CURRENT STATE facts (verified this session).
6. **Conversation search** recovers prior skill/setup discussion.
7. **Research namespaces** hold useful external knowledge (e.g. agent-memory arXiv mappings).
8. **Context-governor** has a large live receipt set and MCP expand path.
9. **SQLite PRAGMA integrity_check = ok** on both stores (DB file not corrupted; operational integrity is the issue).

---

## Critical findings (ranked)

### C1 — Hermes MCP points at legacy store (store split-brain)

- **Evidence**: live `~/.hermes/config.yaml`; processes with `--memory-dir .../local/share/semantic-memory`.
- **Impact**: Hermes interactive tools write a different universe than hooks/Grok/systemd.
- **Remediation**: repoint Hermes MCP to hermes SoR; migrate any post-regression facts; freeze local/share as archive/RO.

### C2 — Schema 36 vs supported 34 (integrity FALSE)

- **Evidence**: `/verify-integrity` on 1738/1739; DB `_schema_version` max **36**; HTTP services started 07:31 with cargo binary that may predate schema 36 migrations applied later.
- **Impact**: index/embedding/sidecar ops unreliable; missing embeddings (16); pending HNSW deletes.
- **Remediation**: one rebuild/install of `semantic-memory-mcp` that supports schema ≥36; restart both systemd units + all MCP clients; re-verify integrity green; reembed-missing; drain HNSW queue.

### C3 — Privilege collapse on Grok host

- **Evidence**: `permission_mode = "always-approve"`; admin MCP always `enabled = true` with full profile.
- **Impact**: dual-rail is procedural (AGENTS.md) not mechanical; full destructive surface co-resident.
- **Remediation**: disable admin by default or require interactive approval for admin/destructive tools; never pair always-approve with full profile for high-assurance use.

### C4 — Warm HTTP is an unprofiled write/maintain surface

- **Evidence**: binary contract (HTTP does not apply MCP tool profile); loopback open to local processes.
- **Impact**: `POST /add` / maintenance can bypass agent capture discipline.
- **Remediation**: coding sidecar read-only (search/health only); token-gate write/maintain; keep “no unattended POST /add” as code not just policy.

---

## High findings

| ID | Finding | Fix direction |
|----|---------|---------------|
| H1 | Stale CURRENT STATE / tool-count facts still rank on broad queries | Supersede pack; search-time demote status language |
| H2 | Two near-duplicate 2026-07-11 Grok dual-rail CURRENT STATE facts | Collapse to one authoritative head + supersede trail |
| H3 | `general` fragment pollution (short bullets, file lists as facts) | Capture gates + curator pass |
| H4 | Kit defaults still encode `~/.local/share` | Fail-closed if DIR unset / wrong |
| H5 | Admin dual-load flaky (Broken pipe at start) | Lazy-start admin; shared embedder; health probe |
| H6 | Denylist `hostile-*` may not prefix-match in recall filter | Implement prefix/glob; unit test fixtures |
| H7 | Claim-ledger not operationalized as shared host artifact | Default ledger root + when-to-use gate |
| H8 | Context-governor dual silos (local/share vs Hermes) | One `CONTEXT_GOVERNOR_STORE` |

**Controller correction to Lane 2:** ASYNC DELEGATION and “Memory updated” patterns are **already 0** in the hermes DB today (junk export from 2026-07-02 is historical). Do not re-count those as live pollution. Live pollution is **fragment capture + stale status heads**, not the old async dumps.

---

## Probe receipts (this session)

| Probe | Result |
|-------|--------|
| `sm_stats` | 657 facts, 954 edges, 18.71 MB, components healthy |
| `sm_list_namespaces` | 24 namespaces |
| Witnessed: “memory system effectiveness” | Top hits = **June** CURRENT STATE (stale tool counts / local-share era) |
| Witnessed: “Grok dual-rail agent admin” | Top hits = **2026-07-11** dual-rail CURRENT STATE (fresh, correct) |
| Witnessed: “canonical store path hermes” | Mix: June path-correct-but-inventory-wrong + July dual-rail |
| Conversation search | Functional |
| SQLite integrity | ok on both DBs |
| CG receipts list | 100+ ids present |

Interpretation: **retrieval is query-sensitive.** The system *can* surface truth when the query names the right era/topic; it does **not** reliably demote superseded-looking status language on generic queries.

---

## Promotion criteria (≥ 7.5 overall)

Treat the memory system as **promotion-ready** only when all of these are green:

- [ ] Hermes MCP `--memory-dir` = hermes SoR; zero agent writers on local/share  
- [ ] `/verify-integrity` integrity true on 1738 and 1739 after binary align  
- [ ] Missing embeddings = 0; HNSW pending ops = 0  
- [ ] Supersession pack complete for infrastructure CURRENT STATE (one head per topic)  
- [ ] Generic “how is my memory configured?” query returns July dual-rail fact as #1 without June tool-count fiction  
- [ ] Admin either default-off or hard-approval for destructive tools  
- [ ] Coding HTTP read-only or token-gated writes  
- [ ] Hostile denylist prefix-match verified with live fixtures  
- [ ] Single context-governor store; claim-ledger root documented and used for material claims  

---

## Priority remediation order

1. Fix Hermes `mcp_servers.semantic_memory` memory-dir → hermes SoR; restart Hermes MCP children  
2. Rebuild/install cargo binary supporting schema 36; restart 1738/1739 + Grok MCPs  
3. Reembed-missing + drain HNSW; confirm integrity true  
4. Supersede infrastructure status pack (June heads → single July dual-rail truth)  
5. Governance: admin default-off or approval gates; read-only coding HTTP  
6. Unify companion stores; curator pass on `general` fragments  
7. Kit defaults fail-closed on wrong DIR  

---

## Lane summaries (abridged)

### Lane 1 — Architecture
Grok’s declared architecture is excellent; runtime SoR is not single. Hermes MCP regression + schema/binary drift dominate. Companions partially unified. Score **4.8**.

### Lane 2 — Retrieval
Search is alive and often topic-relevant; freshness and status-language ranking are the main quality failures. Supersession works as a tool, not as automatic hygiene. Score **5.0** (controller raised noise score slightly after live junk re-scan).

### Lane 3 — Governance
Paper dual-rail is literate; live enforcement soft. Always-approve + always-on admin + unprofiled HTTP writes + dual-store defaults keep adversarial modes open. Score **5.2**.

---

## Final controller claim

> **The new RecursiveIntell dual-rail memory system on Grok is a real, working product surface (search, receipts, dual profiles, warm HTTP, companions) at roughly half of its designed effectiveness.** Policy and Grok wiring are ahead of multi-host runtime hygiene. Fix store unity, schema integrity, and status-fact supersession before trusting it as the shared durable brain across agents.

**Overall: 5.0 / 10**
