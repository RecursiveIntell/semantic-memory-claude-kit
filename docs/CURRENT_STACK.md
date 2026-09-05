# Current RecursiveIntell stack integration

Source inspection: **2026-09-05**. This guide is a source map and kit upgrade
contract, not a claim that every component is installed or tested together.
The machine-readable [source inventory](upstream-sources.json) pins the revisions.

## Resolve source before upgrading

| Component | Inspected source | Meaning for the kits |
|---|---|---|
| Libraries | [`main` at 70e20e6](https://github.com/RecursiveIntell/Libraries/tree/70e20e6cfb9d96b27deedf18dda473643d82f469) | September 2 research integration merged September 4. Default `p32-schema-compat` remains at July 16; explicitly select the source you intend. |
| semantic-memory | [Libraries source](https://github.com/RecursiveIntell/Libraries/tree/70e20e6cfb9d96b27deedf18dda473643d82f469/semantic-memory), manifest `0.5.15` | Contains newer integrity, evidence-gap, state, forgetting and procedural-memory work than standalone `main` at `530b70e`. These are source revisions, not interchangeable release proofs. |
| semantic-memory-mcp | [`main` at 0ac9ca6](https://github.com/RecursiveIntell/semantic-memory-mcp/tree/0ac9ca6e0035df7918da0b9a1c97576b8bee29bb), manifest `0.5.8` | Owns CLI, tool profiles, transport permissions and governed mutation exposure. Its manifest uses sibling path dependencies. |
| context-governor | [Libraries source](https://github.com/RecursiveIntell/Libraries/tree/70e20e6cfb9d96b27deedf18dda473643d82f469/context-governor), manifest `0.2.0` | Owns V2 receipts, lineage, governed keys and prepare/activate recovery. The standalone repository lookup returned 404 during this pass. |
| Mnemes | [`main` at 908c0c2](https://github.com/RecursiveIntell/mnemes/tree/908c0c20fd9ad404cdac4c6845094868a5e6b1e9) | Device/actor configuration, replication, revocation and the native MCP proxy remain upstream. |
| AgentGraph MCP | [`main` at 85346a0](https://github.com/RecursiveIntell/agent-graph-mcp/tree/85346a0ba2cce5f82ac30b21c83993c8f0682716) | Proxy connects to an existing daemon; daemon absence is an error. Build references local Libraries and proveKV paths. |
| Ares | [`main` at f84517f](https://github.com/RecursiveIntell/Ares/tree/f84517ffe96dfdb368011358eed6bda1c0c62996) | Current context-engine adapter and Electron-admitted specialist dispatch are distinct from memory-kit MCP integration. |

No crates.io versions, clean Rust builds, native host installations, live devices,
or performance results were certified in this update. The environment had no
Cargo binary. Do not upgrade by replacing a known working binary with an arbitrary
checkout just because its manifest version matches.

## Latest work and its owner

| Work | Current source evidence | Kit behavior / next activation gate |
|---|---|---|
| Memory integrity and temporal reasoning | `semantic-memory/src/state_epistemics.rs`, `origin_authority.rs`, `evidence_gap.rs`; `tests/dr05_conformance_pack.rs` | Skills preserve historical/current views, authority and abstention. Core API availability must be checked through the connected MCP schema. |
| Forgetting and repair closure | `semantic-memory/src/forgetting.rs`; `tests/forgetting_closure.rs` | Native permit, dependency closure and receipt required. No automatic migration/deletion or Python substitute. |
| Procedural memory and policy promotion | `semantic-memory/src/procedural_memory.rs`, `shadow_policy.rs` | Learned proposals remain advisory; native promotion evidence and permits own admission. No kit-owned promotion store. |
| Atomic capture and replication | `semantic-memory/tests/journal_replication_e2e.rs`; MCP `src/main.rs` Mnemes flags | Launchers forward explicit device/store/epoch/required settings. Operator must separately prove enrollment, sync, replay, offline retrieval and revocation. |
| Context recovery / execution integrity | `context-governor/src/main.rs`, `lineage.rs`, `key_authority.rs` | Probe native `capabilities`. V2 uses governed key/snapshot descriptors, `prepare-v2` and `activate-v2`; legacy kit compaction is not V2 recovery certification. |
| Compressed candidate retrieval | MCP `src/main.rs`; memory `vector_backend.rs`, `quantize_governed.rs` | TurboQuant settings reach the server; the server owns feature checks and exact f32 reranking. Compression does not certify recall or speed superiority. |
| Graph checkpoints and execution receipts | AgentGraph `src/run_manager.rs`, `store.rs`, `evidence.rs` | Optional existing daemon connection only. A memory receipt cannot authorize execution or substitute for a graph checkpoint. |
| Sparse specialist collaboration | Ares `ares_runtime/specialist_routing.py`, `specialist_dispatch.py` | Nonactivation selection cannot dispatch; explicit dispatch needs Electron admission and profile bindings. Kits add no competing dispatcher. |
| Context-engine integration | Ares `plugins/context_engine/ri-context-governor/__init__.py` | Ares owns configured engine `ri-context-governor`; adding a companion MCP server is not activating that engine. |
| Evidence and evaluation | kit native audit wrapper and tool-surface probe | Native receipts pass through unchanged. Missing owners produce typed failure. Tools/list probes initialize, correlate responses and use disposable mock stores. External datasets are explicit optional gates. |

Rows describe inspected source and bounded kit changes. Named upstream tests were
inspected as evidence targets, not reported as locally passing. This is not a full
DR-01–DR-20 implementation certification or an audit of every repository.

## Configuration that reaches the native server

Shared/Codex/Claude/Hermes launchers use the same generated implementation. Set values in
the host's environment/configuration, then restart that host. The launchers never
provision credentials or rewrite an existing database.

| Environment variable | CLI option / behavior |
|---|---|
| `SEMANTIC_MEMORY_MCP_BIN` | Explicit executable; invalid selection fails. Otherwise PATH, then `~/.local/bin`, then `~/.cargo/bin`. |
| `SEMANTIC_MEMORY_DIR` | `--memory-dir`; a directory, even when its name ends in `.db`. A file at this path fails. |
| `SEMANTIC_MEMORY_EMBEDDER` | `--embedder`; defaults to `candle`; set `ollama` explicitly. |
| `SEMANTIC_MEMORY_EMBEDDING_URL` / `MODEL` / `DIMS` | `--embedding-url` / `--embedding-model` / `--embedding-dims` (full variable prefix applies to each). |
| `SEMANTIC_MEMORY_TOOL_PROFILE` | `--tool-profile`; shared/Hermes defaults to `lean`, Codex/Claude to `agent`. `stable`, `standard`, `full` are passed to the native owner too. |
| `SEMANTIC_MEMORY_OPERATOR_AUTHORITY_TOKEN_FILE` | `--operator-authority-token-file`; does not create a permit or grant host authority. |
| `SEMANTIC_MEMORY_HTTP_PORT` | `--http-port` only if explicitly nonzero; default is stdio only. |
| `SEMANTIC_MEMORY_HTTP_AUTH_TOKEN_FILE` | `--http-auth-token-file`; private token file validated by upstream. |
| `SEMANTIC_MEMORY_MCP_HTTP_PORT` / `SEMANTIC_MEMORY_MCP_HTTP_TOKEN_FILE` | `--mcp-http-port` / `--mcp-http-token-file`; explicit upstream Streamable HTTP configuration. |
| `SEMANTIC_MEMORY_TURBO_QUANT` | `--turbo-quant` for `1` or `true`; invalid boolean rejected. |
| `SEMANTIC_MEMORY_TURBO_QUANT_BITS` / `PROJECTIONS` | `--turbo-quant-bits` / `--turbo-quant-projections` (full variable prefix applies). |
| `SEMANTIC_MEMORY_MNEMES_DEVICE_ID` / `STORE_ID` / `STREAM_EPOCH` | Native `--mnemes-*` identity options; no enrollment or epoch changes are inferred. |
| `SEMANTIC_MEMORY_MNEMES_REQUIRED` | `--mnemes-required` for `1` or `true`; native server checks required identity. |

An explicitly requested unsupported option fails before server startup. The
current inspected MCP source does not expose `--llm-model`: an explicit
`SEMANTIC_MEMORY_LLM_MODEL` setting therefore fails with an actionable option error.
The kits no longer inject an arbitrary LLM model by default.

Legacy Hermes `SEMANTIC_MEMORY_HTTP_TOKEN` and `SEMANTIC_MEMORY_HTTP_TOKEN_FILE`
settings are rejected at its shell entrypoint. Use the canonical
`SEMANTIC_MEMORY_HTTP_AUTH_TOKEN_FILE` setting with a private file. Token values
must not be put directly on the command line.

### Store and transport upgrade boundaries

- Shared and Codex server launcher defaults remain `~/.local/share/semantic-memory`.
  Claude remains `~/.hermes/semantic-memory.db`. Existing Codex recall hooks use
  the latter path; **set `SEMANTIC_MEMORY_DIR` consistently for both hooks and MCP**
  before relying on shared recall. This update does not silently move or merge stores.
- Claude's machine-specific relay and fixed relay ports were removed. An old
  `SEMANTIC_MEMORY_RELAY_PORT` setting is rejected. Configure any existing upstream
  relay or Streamable HTTP transport explicitly; do not point a new local process
  at a live store already owned by a remote service without checking ownership.
- Daily MCP profiles are not an HTTP bypass. At the inspected revision, non-health
  HTTP routes require the native full profile and transport authentication. Never
  widen to full just to make a legacy warm hook work. Legacy HTTP hooks are not
  certified against the new authenticated transport in this pass; use witnessed
  MCP retrieval and validate your host-specific hook integration separately.
- Admin launch starts a process only. It no longer manufactures a `reembed_missing`
  receipt merely because an admin server was started. Native operation receipts
  belong to the operations actually invoked.

## Optional companion connections

Mnemes already supplies `scripts/mneme-mcp-proxy.py` with its sibling
`mneme-client.py`. Configure its upstream client environment (`MNEMES_ENV_FILE`
or the URL/credential/actor/device settings) and run its own enrollment and
revocation checks. Do not copy credential values into the kit or commit them.

AgentGraph uses `agent-graph-mcpd` plus the `agent-graph-mcp` proxy. Inspect the
selected build's CLI and daemon recovery tests; do not launch deprecated direct
mode or auto-start a daemon from a memory hook. Its local path dependencies need
a separate clean-build proof before recommending installation to other users.

## Validation and rollback

```bash
python3 -m pip install -r tests/requirements.txt
python3 scripts/sync-kit-assets.py --check
python3 -m pytest -q -rs
./scripts/validate-all-kits.sh --static
# On an installed host, separately:
./scripts/validate-all-kits.sh --native
```

Native governor integration tests require `CONTEXT_GOVERNOR_BIN`; official STALE
tests require `.bench-data/stale/T1_T2_400_FULL.json`. Skips are unproven gates,
not passing benchmarks. The separate missing-owner regression tests always run.

Revert the kit update commit to restore source and plugin payloads. No existing
store, replica, device membership, key, daemon or host configuration was modified.
Before any native binary upgrade, use that owner's backup, migration and restore
procedure; reverting kit source does not reverse a native store migration.
