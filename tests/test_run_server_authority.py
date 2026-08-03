#!/usr/bin/env python3
from __future__ import annotations

import os
import subprocess
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RUN_SERVER = ROOT / "shared/scripts/run-server.sh"


class RunServerAuthorityTests(unittest.TestCase):
    def test_forwards_explicit_operator_authority_token_file_for_agent_profile(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            binary = tmp_path / "semantic-memory-mcp"
            captured_args = tmp_path / "captured-args.txt"
            token_file = tmp_path / "operator-authority.token"
            token_file.write_text("test-only-token\n", encoding="utf-8")
            binary.write_text(
                "#!/usr/bin/env sh\n"
                "if [ \"${1:-}\" = \"--help\" ]; then\n"
                "  printf '%s\\n' '--tool-profile --http-port --operator-authority-token-file'\n"
                "  exit 0\n"
                "fi\n"
                "printf '%s\\n' \"$@\" > \"$CAPTURE_ARGS\"\n",
                encoding="utf-8",
            )
            binary.chmod(0o755)
            env = os.environ.copy()
            env.update(
                {
                    "SEMANTIC_MEMORY_MCP_BIN": str(binary),
                    "SEMANTIC_MEMORY_DIR": str(tmp_path / "memory"),
                    "SEMANTIC_MEMORY_HTTP_PORT": "0",
                    "SEMANTIC_MEMORY_TOOL_PROFILE": "agent",
                    "SEMANTIC_MEMORY_OPERATOR_AUTHORITY_TOKEN_FILE": str(token_file),
                    "CAPTURE_ARGS": str(captured_args),
                }
            )
            result = subprocess.run(
                [str(RUN_SERVER)],
                text=True,
                capture_output=True,
                timeout=15,
                env=env,
                check=False,
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            args = captured_args.read_text(encoding="utf-8").splitlines()
            self.assertIn("--tool-profile", args)
            self.assertIn("agent", args)
            self.assertIn("--operator-authority-token-file", args)
            self.assertIn(str(token_file), args)
            self.assertNotIn("test-only-token", args)


if __name__ == "__main__":
    unittest.main()
