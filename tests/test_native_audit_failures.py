"""A kit wrapper cannot certify a missing or failed native governor."""
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

SCRIPT = Path(__file__).resolve().parents[1] / 'shared/scripts/context-governor-audit.py'
class NativeAuditFailureTests(unittest.TestCase):
    def invoke(self, binary, *args):
        return subprocess.run([sys.executable,str(SCRIPT),'--binary-path',str(binary),*args],text=True,capture_output=True,timeout=10)

    def test_missing_native_owner_is_not_a_pass(self):
        for command,args in [('select-route',['--query','test']),('audit-compression-boundary',['--request-json',json.dumps({'source_fragments':['evidence'],'compressed_summary':'summary'})])]:
            result = self.invoke('/missing/native',command,*args)
            self.assertEqual(result.returncode,127)
            data=json.loads(result.stdout)
            self.assertEqual(data['code'],'OWNER_UNAVAILABLE')
            self.assertNotIn('passed',data)

    def test_invalid_boundary_is_rejected_without_substitution(self):
        result=self.invoke('/missing/native','audit-compression-boundary','--request-json','{"source_text":"old alias"}')
        self.assertEqual(result.returncode,64)
        self.assertEqual(json.loads(result.stdout)['code'],'INVALID_REQUEST')

    def test_native_failure_malformed_and_valid_receipt(self):
        for output,exit_code,expected in [('bad-json',0,'INVALID_OWNER_RESPONSE'),('{}',0,'INVALID_OWNER_RESPONSE'),('',4,'OWNER_FAILED'),('{"schema":"NativeReceiptV1","passed":false}',0,None)]:
            with tempfile.TemporaryDirectory() as tmp:
                binary=Path(tmp)/'governor'
                binary.write_text('#!/usr/bin/env python3\n'+f'print({output!r})\nraise SystemExit({exit_code})\n');binary.chmod(0o755)
                result=self.invoke(binary,'select-route','--query','test')
                if expected:
                    self.assertNotEqual(result.returncode,0)
                    self.assertEqual(json.loads(result.stdout)['code'],expected)
                else:
                    self.assertEqual(result.returncode,0)
                    self.assertEqual(json.loads(result.stdout),json.loads(output))
