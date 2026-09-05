"""Process-boundary regressions for all distributed launchers, without live stores."""
import json
import os
from pathlib import Path
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
LAUNCHERS = [ROOT / 'shared/scripts/run-server.sh', ROOT / 'hermes/scripts/run-server.sh'] + [ROOT / host / 'plugins/semantic-memory/scripts/run-server.sh' for host in ('codex', 'claude')]
FLAGS = '--memory-dir --embedder --tool-profile --embedding-url --embedding-model --embedding-dims --operator-authority-token-file --http-auth-token-file --http-port --mcp-http-port --mcp-http-token-file --turbo-quant --turbo-quant-bits --turbo-quant-projections --mnemes-device-id --mnemes-store-id --mnemes-stream-epoch --mnemes-required'

class CurrentStackLaunchTests(unittest.TestCase):
    def run_launcher(self, launcher, settings=None, flags=FLAGS, extra=()):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            binary = root / 'server with spaces'
            capture = root / 'args.json'
            binary.write_text('#!/usr/bin/env python3\nimport json,os,sys\nif sys.argv[1:]==["--help"]:\n print(os.environ["FLAGS"])\n sys.exit(0)\nopen(os.environ["CAPTURE"],"w").write(json.dumps(sys.argv[1:]))\nsys.exit(int(os.environ.get("SERVER_EXIT","0")))\n')
            binary.chmod(0o755)
            env = {k:v for k,v in os.environ.items() if not k.startswith(('SEMANTIC_MEMORY_', 'SM_KIT_', 'SM_TURBO_QUANT'))}
            env.update(HOME=temp, SEMANTIC_MEMORY_MCP_BIN=str(binary), CAPTURE=str(capture), FLAGS=flags)
            env.update(settings or {})
            proc = subprocess.run([str(launcher), *extra], env=env, text=True, capture_output=True, timeout=10)
            argv = json.loads(capture.read_text()) if capture.exists() else None
            return proc, argv

    def test_host_defaults_preserved_without_implicit_http(self):
        for launcher in LAUNCHERS:
            with self.subTest(launcher=launcher):
                proc, argv = self.run_launcher(launcher)
                self.assertEqual(proc.returncode, 0, proc.stderr)
                self.assertNotIn('--http-port', argv)
                self.assertNotIn('--operator-authority-token-file', argv)
                profile = argv[argv.index('--tool-profile') + 1]
                self.assertEqual(profile, 'lean' if any(x in launcher.parts for x in ('shared','hermes')) else 'agent')
                suffix = '/.hermes/semantic-memory.db' if 'claude' in launcher.parts else '/.local/share/semantic-memory'
                self.assertTrue(argv[1].endswith(suffix))

    def test_forwards_embedding_authority_codec_and_journal_configuration(self):
        settings = {'SEMANTIC_MEMORY_EMBEDDER':'ollama', 'SEMANTIC_MEMORY_EMBEDDING_URL':'http://localhost:11434', 'SEMANTIC_MEMORY_EMBEDDING_MODEL':'test-model', 'SEMANTIC_MEMORY_EMBEDDING_DIMS':'768', 'SEMANTIC_MEMORY_OPERATOR_AUTHORITY_TOKEN_FILE':'/private/operator.token', 'SEMANTIC_MEMORY_HTTP_AUTH_TOKEN_FILE':'/private/http.token', 'SEMANTIC_MEMORY_HTTP_PORT':'1739', 'SEMANTIC_MEMORY_MCP_HTTP_PORT':'1742', 'SEMANTIC_MEMORY_MCP_HTTP_TOKEN_FILE':'/private/mcp.token', 'SEMANTIC_MEMORY_TURBO_QUANT':'true', 'SEMANTIC_MEMORY_TURBO_QUANT_BITS':'8', 'SEMANTIC_MEMORY_TURBO_QUANT_PROJECTIONS':'16', 'SEMANTIC_MEMORY_MNEMES_DEVICE_ID':'fixture-device', 'SEMANTIC_MEMORY_MNEMES_STORE_ID':'fixture-store', 'SEMANTIC_MEMORY_MNEMES_STREAM_EPOCH':'2', 'SEMANTIC_MEMORY_MNEMES_REQUIRED':'1'}
        for launcher in LAUNCHERS:
            proc, argv = self.run_launcher(launcher, settings)
            self.assertEqual(proc.returncode,0,proc.stderr)
            for flag in FLAGS.split(): self.assertIn(flag,argv)
            for value in set(settings.values())-{'true','1'}: self.assertIn(value,argv)
            self.assertIn('--mnemes-required',argv)

    def test_missing_option_and_help_prefix_fail_before_start(self):
        for launcher in LAUNCHERS:
            for flags in (FLAGS.replace('--operator-authority-token-file',''), FLAGS.replace('--operator-authority-token-file','--operator-authority-token-file-extra')):
                proc, argv = self.run_launcher(launcher, {'SEMANTIC_MEMORY_OPERATOR_AUTHORITY_TOKEN_FILE':'/private/token'}, flags)
                self.assertEqual(proc.returncode,64)
                self.assertIsNone(argv)
                self.assertIn('--operator-authority-token-file',proc.stderr)

    def test_invalid_explicit_binary_relay_boolean_and_store_fail_closed(self):
        for settings in ({'SEMANTIC_MEMORY_MCP_BIN':'/nonexistent'}, {'SEMANTIC_MEMORY_RELAY_PORT':'17540'}, {'SEMANTIC_MEMORY_TURBO_QUANT':'yes'}, {'SEMANTIC_MEMORY_DIR':str(__file__)}):
            proc, argv = self.run_launcher(LAUNCHERS[0],settings)
            self.assertNotEqual(proc.returncode,0)
            self.assertIsNone(argv)

    def test_admin_preserves_server_failure_and_emits_no_fake_operation_receipt(self):
        for launcher in LAUNCHERS:
            proc, argv = self.run_launcher(launcher.with_name('run-server-admin.sh'), {'SERVER_EXIT':'23'})
            self.assertEqual(proc.returncode,23)
            self.assertEqual(argv[argv.index('--tool-profile')+1], 'full')
            self.assertEqual(proc.stdout,'')

    def test_hermes_rejects_legacy_credentials_without_leaking_them(self):
        launcher = ROOT / 'hermes/scripts/run-server.sh'
        for settings,extra in [({'SEMANTIC_MEMORY_HTTP_TOKEN':'secret-value'},()),
                               ({},('--http-auth-token=secret-value',))]:
            proc,argv = self.run_launcher(launcher,settings,extra=extra)
            self.assertEqual(proc.returncode,64)
            self.assertIsNone(argv)
            self.assertNotIn('secret-value',proc.stdout+proc.stderr)

    def test_fresh_host_configs_do_not_enable_unauthenticated_http(self):
        import importlib.util
        spec = importlib.util.spec_from_file_location('setup_host', ROOT/'shared/scripts/setup-host.py')
        setup = importlib.util.module_from_spec(spec); spec.loader.exec_module(setup)
        from unittest import mock
        with mock.patch.dict(os.environ, {}, clear=True):
            for host in setup.HOST_CONFIG:
                config = setup.mcp_config(host)
                self.assertEqual(config['mcpServers']['semantic-memory']['env']['SEMANTIC_MEMORY_HTTP_PORT'], '0')
        paths = list(ROOT.glob('*/mcp*.json.example')) + [ROOT/'continue/config.json.example', ROOT/'opencode/opencode.json.example', ROOT/'shared/snippets/mcp-stdio.json']
        for path in paths:
            config = json.loads(path.read_text())
            self.assertEqual(config['mcpServers']['semantic-memory']['env']['SEMANTIC_MEMORY_HTTP_PORT'], '0')

    def test_distributed_assets_are_current(self):
        subprocess.run(['python3',str(ROOT/'scripts/sync-kit-assets.py'),'--check'],check=True,capture_output=True)
