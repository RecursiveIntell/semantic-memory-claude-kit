---
name: memory-capture
description: Persist durable sourced facts to semantic memory when the user asks to remember a decision, preference, correction, or verified project fact. Excludes transient progress, secrets and unverified claims.
---

# Memory capture

1. Discover the connected tools and their schemas. Prefer `sm_search_witnessed`
   for deduplication; inspect close matches with `sm_get_fact` when available.
   Do not assume `sm_search`, `sm_list_facts`, or admin tools exist in the daily
   profile. If retrieval is unavailable, report the gap before writing duplicates.
2. Preserve namespace, subject and source identity. Store concise durable content
   with the provenance required by the native API. Keep valid time distinct from
   recorded time; do not invent either from a summary.
3. If `sm_add_fact` is exposed and the requested capture is authorized, call it
   using the actual schema. Missing operator authority is a blocked write, not a
   reason to retry with broader privileges. Do not persist secrets or credentials.
4. For a correction, prefer `sm_supersede_fact` only when exposed and authorized.
   Otherwise report the proposed replacement and the unavailable operation.
   Do not replace native supersession with a `supersedes` graph edge or overwrite.
5. Report the returned fact ID, namespace and native receipt/evidence references.
   If persistence failed, say so. Tool exposure and process startup are not proof
   that a fact was stored.

For historical assertions, governed maintenance or recovery, read the sibling
[governed-memory skill](../governed-memory/SKILL.md). Current source evidence
outranks memory. Save lasting decisions, not temporary TODOs or routine run logs.
