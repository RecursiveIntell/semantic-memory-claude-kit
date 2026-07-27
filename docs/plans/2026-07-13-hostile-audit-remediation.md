# Unified Remediation Plan — Hostile Audits 2026-07-13

**Targets:** agent-memory-kits, semantic-memory-mcp  
**Authority:** fresh source and fresh commands outrank prior receipts.

## Already Fixed (prior session)

| ID | Fix | Receipt |
|---|---|---|
| KIT-001 | SM_AUTO_INGEST defaults to 0 | `codebase-auto-ingest.py` line 1 |
| KIT-003 | drop_superseded_hits returns fresh unconditionally | `common.py` |
| KIT-004 | SM_RECALL_RECORD_OUTCOME defaults to "0" | `memory-recall.py` line 205 |
| KIT-005 | freshness_rank removed | `memory-recall.py` lines 236-239 |
| KIT-007 | Hash-based namespace (sha256 of root path) | `codebase-auto-ingest.py` |
| MCP-003 | top_k capped at 100 in /search, /search-routed | `http_server.rs` |
| MCP-009 | Rerank error handling — no longer fabricates 1.0 | `http_server.rs` |

## Remaining Fixes

### agent-memory-kits

| ID | Severity | What | Fix | RED gate |
|---|---|---|---|---|
| KIT-002 | P0 | Codex recall uses unwitnessed HTTP search; Hermes uses witnessed + provenance admission | Wire Codex recall through `admit_provenanced_hits` + `frame_hits` from shared `injection_framing.py` | Codex recall path produces inert framed hits with provenance |
| KIT-006 | P1 | Codex and Hermes have independently copied recall with different safety | Extract shared host-neutral retrieval core; host adapters only handle payload/output shapes | One parameterized host-contract suite rejects incomplete provenance for every host |
| NEW P1 | P1 | Setup/installer/hooks use `~/.local/share/semantic-memory`; doctor checks `~/.hermes/semantic-memory.db` | One shared default-store resolver used by all entry points | setup, installer, hooks, and doctor resolve the same default path |

### semantic-memory-mcp

| ID | Severity | What | Fix | RED gate |
|---|---|---|---|---|
| MCP-002 | P0 | sm_delete_namespace executes without auth (sm_delete_fact already fails closed) | Gate sm_delete_namespace same as sm_delete_fact — fail closed with "no trusted authenticated authority issuer" | sm_delete_namespace returns BLOCKED error |
| MCP-004 | P1 | sm_insert_fact allows arbitrary namespace injection | Validate namespace against allowed list or require explicit namespace registration | Unregistered namespace returns 400 |
| MCP-006 | P1 | sm_search returns raw content without provenance framing | Add provenance fields (source, trust, retrieval_receipt_ref) to search results | Every search hit has source + trust + receipt_ref |
| MCP-008 | P2 | Community summarization returns text with no model/prompt digest or receipt | Attach execution receipt with model/prompt digests and status | Summary response has receipt/status field |
| MCP-010 | P2 | Tool counts drift: README says 16, manifest has 11, Cargo.toml says 18 | Generate profile lists from manifest; remove hardcoded counts | Documentation/profile consistency check passes |

## Implementation Order

1. **KIT-002** (P0) — Wire Codex recall through witnessed path
2. **MCP-002** (P0) — Gate sm_delete_namespace
3. **MCP-004** (P1) — Namespace validation
4. **MCP-006** (P1) — Provenance framing in search results
5. **KIT-006** (P1) — Shared retrieval core
6. **NEW P1** (kits) — Default store resolver
7. **MCP-008** (P2) — Community summary receipt
8. **MCP-010** (P2) — Tool count consistency

## Claim Boundary

This plan does not certify production behavior, broad autonomy, or cloud readiness. Certification can be reconsidered only after the fresh command bar is green.
