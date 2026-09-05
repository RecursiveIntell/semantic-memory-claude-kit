"""Doctor must test the selected configuration, not silently substitute defaults."""
import importlib.util
import json
import os
from pathlib import Path
import tempfile
import unittest
from unittest import mock

ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('doctor_config',ROOT/'shared/scripts/doctor_core.py')
doctor=importlib.util.module_from_spec(spec);spec.loader.exec_module(doctor)
TOOLS=['sm_search_witnessed','sm_replay_search','sm_decide_assertion_authority','sm_decide_action_authority']

class DoctorConfigurationTests(unittest.TestCase):
    def test_configuration_forwarded_and_unsupported_flags_cannot_pass(self):
        for supports in (True,False):
            with tempfile.TemporaryDirectory() as tmp:
                root=Path(tmp);binary=root/'fixture';captured=root/'argv'
                flags='--memory-dir --embedder --tool-profile --embedding-model --embedding-dims --mnemes-device-id'
                if supports:flags+=' --mnemes-required'
                response=json.dumps({'id':2,'result':{'tools':[{'name':name} for name in TOOLS]}})
                binary.write_text('#!/usr/bin/env python3\nimport sys,json\n'+f'if sys.argv[1:]==["--help"]:\n print({flags!r})\n sys.exit(0)\n'+f'open({str(captured)!r},"w").write(json.dumps(sys.argv[1:]))\nprint({response!r})\n')
                binary.chmod(0o755)
                env={k:v for k,v in os.environ.items() if not k.startswith('SEMANTIC_MEMORY_')}
                env.update(SEMANTIC_MEMORY_EMBEDDING_MODEL='fixture-model',SEMANTIC_MEMORY_EMBEDDING_DIMS='384',SEMANTIC_MEMORY_MNEMES_DEVICE_ID='fixture-device',SEMANTIC_MEMORY_MNEMES_REQUIRED='1',SEMANTIC_MEMORY_HTTP_PORT='1739')
                with mock.patch.dict(os.environ,env,clear=True),mock.patch.object(doctor,'MEMORY_DIR',root/'store'):
                    self.assertEqual(doctor.rpc_tools_list(binary),supports)
                if supports:
                    args=json.loads(captured.read_text())
                    for value in ('--mnemes-required','fixture-device','fixture-model','384'):self.assertIn(value,args)
                    self.assertNotIn('--http-port',args)
                else:self.assertFalse(captured.exists())
