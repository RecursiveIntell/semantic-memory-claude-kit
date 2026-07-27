#!/usr/bin/env python3
from __future__ import annotations

import sys

sys.dont_write_bytecode = True

from common import debug


def main() -> int:
    debug("Stop semantic-memory capture nudge")
    print(
        "Semantic memory reminder: Codex may append only compact, verified, active-repository coding facts "
        "to that repository's collision-safe namespace after scoped dedupe and current source/test evidence. "
        "Do not write architecture guesses or broad decisions; return those as memory_candidates for controller review. "
        "Never write personal/global memory, secrets, logs, TODOs, session state, or mutate/supersede/delete/govern memory.",
        file=sys.stderr,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
