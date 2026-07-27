# Unified Remediation Plan — 2026-07-13 Hostile Audits

**Targets:**
- `/home/sikmindz/Coding/agent-memory-kits` (Codex audit: 7 KIT issues + 1 new P1)
- `/home/sikmindz/Coding/Libraries/semantic-memory-mcp` (Codex audit: 10 MCP issues + 1 new P1)

**Authority:** Fresh source and fresh commands outrank prior receipts.

---

## Phase 1: CRITICAL — Safety fixes (P0)

### Task 1.1: KIT-001 — Default auto-ingest to OFF
**File:** `codex/plugins/semantic-memory/hooks/codebase-auto-ingest.py:249`
**Change:** `os.environ.get("SM_AUTO_INGEST", "1")` → `os.environ.get("SM_AUTO_INGEST", "0")`
**Also:** Update README.md:98 to document default `0`.
**Gate:** `grep "SM_AUTO_INGEST.*\"1\"" codebase-auto-ingest.py` returns nothing.

### Task 1.2: KIT-002 — Codex recall must use witnessed retrieval + provenance admission
**Files:**
- `codex/plugins/semantic-memory/hooks/memory-recall.py` — replace unwitnessed HTTP search with `sm_search_witnessed` RPC, import `injection_framing.py`, use `propagate_retrieval_context` + `admit_provenanced_hits` + `frame_hits`
- `tests/test_codex_memory_recall.py` — add test that incomplete provenance produces no hook context
**Gate:** `python3 -m pytest tests/test_codex_memory_recall.py -v` passes.

### Task 1.3: MCP-001 — Reject caller-controlled fact_id on sm_add_fact
**File:** `src/server.rs` (sm_add_fact handler)
**Change:** If `fact_id` is present in arguments, return error "fact_id is server-assigned; omit it."
**Gate:** `cargo test -p semantic-memory-mcp` passes.

### Task 1.4: MCP-002 — Require authorization for sm_delete_fact / sm_delete_namespace
**File:** `src/server.rs` (delete handlers)
**Change:** Gate on `--tool-profile` — only `full` profile exposes delete tools. Lean/standard profiles omit them.
**Gate:** `cargo test -p semantic-memory-mcp` passes.

---

## Phase 2: HIGH — Data integrity (P1)

### Task 2.1: KIT-003 — drop_superseded_hits must not reintroduce all-stale sets
**File:** `codex/plugins/semantic-memory/hooks/common.py:166-171`
**Change:** `return fresh or hits` → `return fresh`
**Gate:** `python3 -m pytest tests/test_codex_memory_recall.py -v` passes.

### Task 2.2: KIT-004 — Disable self-reinforcing router outcome learning
**File:** `codex/plugins/semantic-memory/hooks/memory-recall.py:196-225`
**Change:** Remove `record_route_outcome()` and `record_routing_outcome()` calls from normal recall path. Keep the functions but don't call them.
**Gate:** `python3 -m pytest tests/test_codex_memory_recall.py -v` passes.

### Task 2.3: KIT-005 — Remove freshness_rank date-string heuristic
**File:** `codex/plugins/semantic-memory/hooks/memory-recall.py:228-236,301-307`
**Change:** Delete `freshness_rank()` function and its call site. Use server-provided validity metadata instead.
**Gate:** `python3 -m pytest tests/test_codex_memory_recall.py -v` passes.

### Task 2.4: KIT-007 — Hash-based namespace for auto-ingest
**File:** `codex/plugins/semantic-memory/hooks/codebase-auto-ingest.py:274`
**Change:** `f"code:{slug(root.name)}"` → `f"code:{slug(root.name)}-{hashlib.sha256(str(root).encode()).hexdigest()[:12]}"`
**Gate:** Two distinct repos `/tmp/a` and `/tmp/b` produce different namespaces.

### Task 2.5: NEW P1 (kits) — Unify default store path
**Files:**
- `codex/plugins/semantic-memory/scripts/setup.sh:6`
- `codex/plugins/semantic-memory/scripts/install-global-config.py:18`
- `codex/plugins/semantic-memory/hooks/common.py:62-64`
- `codex/plugins/semantic-memory/scripts/doctor.py:18`
**Change:** All resolve to `~/.local/share/semantic-memory` (the canonical path). Doctor must match.
**Gate:** `grep -r "semantic-memory.db" codex/` returns only the canonical path.

### Task 2.6: MCP-003 + NEW P1 (mcp) — Cap top_k to prevent overflow/DoS
**File:** `src/http_server.rs` (search, search-routed, discord handlers)
**Change:** Add `const MAX_TOP_K: u64 = 400;` and clamp `top_k` before conversion to usize.
**Gate:** `cargo test -p semantic-memory-mcp` passes.

### Task 2.7: MCP-005 — sm_supersede_fact must verify old fact exists
**File:** `src/server.rs` (sm_supersede_fact handler)
**Change:** Before creating supersession edge, verify `old_fact_id` exists in the store. Return error if not found.
**Gate:** `cargo test -p semantic-memory-mcp` passes.

### Task 2.8: MCP-006 — sm_search_witnessed must persist receipt
**File:** `src/server.rs` (sm_search_witnessed handler)
**Change:** Write receipt to durable store before returning. Currently returns receipt but doesn't persist.
**Gate:** `cargo test -p semantic-memory-mcp` passes.

### Task 2.9: MCP-009 — Rerank must not fabricate scores on failure
**File:** `src/http_server.rs:48-65`
**Change:** On Ollama/network/parse failure, preserve original ranking and mark rerank unavailable. Do NOT return score 1.0.
**Gate:** `cargo test -p semantic-memory-mcp` passes.

---

## Phase 3: MEDIUM — Quality (P2)

### Task 3.1: KIT-006 — Extract shared host-neutral retrieval/admission core
**Files:**
- `shared/scripts/injection_framing.py` — already exists, ensure it's the single source
- `codex/plugins/semantic-memory/hooks/memory-recall.py` — import and use shared core
- `hermes/hooks/sm-recall.py` — already uses it, verify
- `tests/test_injection_framing.py` — add parameterized host-contract test
**Gate:** `python3 -m pytest tests/test_injection_framing.py -v` passes.

### Task 3.2: MCP-004 — Cap sm_ingest_document content size
**File:** `src/server.rs` (sm_ingest_document handler)
**Change:** Reject content > 10MB with clear error.
**Gate:** `cargo test -p semantic-memory-mcp` passes.

### Task 3.3: MCP-007 — Require source field on sm_add_fact
**File:** `src/server.rs` (sm_add_fact handler)
**Change:** If `source` is empty/missing, return error "source is required."
**Gate:** `cargo test -p semantic-memory-mcp` passes.

### Task 3.4: MCP-008 — Attach receipt to community summarization
**File:** `src/server.rs:3717-3771`
**Change:** Add `model_digest`, `prompt_digest`, `execution_status` fields to summary response.
**Gate:** `cargo test -p semantic-memory-mcp` passes.

### Task 3.5: MCP-010 — Fix tool count drift
**Files:** `README.md`, `Cargo.toml`
**Change:** Remove hardcoded counts. Replace with "see profile manifest" or generate from source.
**Gate:** `grep -E "[0-9]+ tools" README.md Cargo.toml` returns no hardcoded counts.

---

## Phase 4: Verification gauntlet

### agent-memory-kits
```bash
cd /home/sikmindz/Coding/agent-memory-kits
python3 -m pytest tests/ -v --tb=short 2>&1 | tail -20
```

### semantic-memory-mcp
```bash
cd /home/sikmindz/Coding/Libraries/semantic-memory-mcp
cargo test --no-fail-fast 2>&1 | grep -E "(test result|FAILED|^error)"
```

---

## Claim boundary

This plan addresses all 18 confirmed audit findings (7 KIT + 10 MCP + 2 new P1s).
It does NOT add new features, change public APIs, or expand provider surfaces.
Certification requires the full verification gauntlet to be green.
