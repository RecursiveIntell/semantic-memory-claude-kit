import importlib.util
import json
from pathlib import Path
import subprocess
import unittest
from unittest import mock

SCRIPT = Path(__file__).resolve().parents[1]/'shared/scripts/generate-tool-surface-docs.py'
spec=importlib.util.spec_from_file_location('surface',SCRIPT)
surface=importlib.util.module_from_spec(spec);spec.loader.exec_module(surface)

class DiscoveryProtocolTests(unittest.TestCase):
    def test_initialize_notification_and_correlated_tools_response(self):
        def run(command, **kwargs):
            messages=[json.loads(line) for line in kwargs['input'].splitlines()]
            self.assertEqual([m['method'] for m in messages],['initialize','notifications/initialized','tools/list'])
            self.assertTrue(kwargs['input'].endswith('\n'))
            return subprocess.CompletedProcess(command,0, '\n'.join([json.dumps({'id':1,'result':{'tools':[{'name':'wrong'}]}}),json.dumps({'id':2,'result':{'tools':[{'name':'right'}]}})]),'')
        with mock.patch.object(surface.subprocess,'run',side_effect=run):
            self.assertEqual(surface.get_mcp_tool_list('fixture',[]),[{'name':'right'}])

    def test_profile_probe_uses_disposable_mock_store(self):
        paths=[]
        def probe(binary,args):
            paths.append(Path(args[args.index('--memory-dir')+1]))
            self.assertTrue(paths[-1].is_dir())
            self.assertEqual(args[args.index('--embedder')+1],'mock')
            return []
        with mock.patch.object(surface,'get_mcp_tool_list',side_effect=probe):
            self.assertTrue(surface.get_profile_tools('agent',str(SCRIPT))['available'])
        self.assertFalse(paths[0].exists())
