import io
import json
from contextlib import redirect_stdout
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest
from file_integrity import snapshot,compare,validate,main

class ManifestTests(unittest.TestCase):
    def test_change_categories(self):
        with TemporaryDirectory() as directory:
            root=Path(directory)
            (root/'keep').write_bytes(b'one'); (root/'remove').write_bytes(b'two')
            before=snapshot(root)
            (root/'keep').write_bytes(b'new'); (root/'remove').unlink(); (root/'added').write_bytes(b'')
            self.assertEqual(compare(before,snapshot(root)),{'added':['added'],'removed':['remove'],'changed':['keep']})
    def test_deterministic_unicode_and_hash(self):
        with TemporaryDirectory() as directory:
            root=Path(directory); (root/'ação.txt').write_bytes(b'abc')
            result=snapshot(root)
            self.assertEqual(result,snapshot(root))
            self.assertEqual(result['files']['ação.txt']['sha256'],'ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad')
    def test_empty(self):
        with TemporaryDirectory() as directory:
            result=snapshot(directory); self.assertEqual(result,{'version':1,'files':{}})
    def test_invalid_manifests(self):
        for name in ['../escape','/absolute','a/../b','a//b','a\\b','.']:
            with self.assertRaises(ValueError): validate({'version':1,'files':{name:{'size':1,'sha256':'0'*64}}})
        with self.assertRaises(ValueError): validate({'version':1,'files':{'x':{'size':True,'sha256':'bad'}}})
    def test_symlink_rejected(self):
        with TemporaryDirectory() as directory:
            root=Path(directory); (root/'real').write_text('x')
            try: (root/'link').symlink_to(root/'real')
            except (OSError,NotImplementedError): self.skipTest('symlinks unavailable')
            with self.assertRaises(ValueError): snapshot(root)
    def test_cli(self):
        with TemporaryDirectory() as directory:
            root=Path(directory)/'data'; root.mkdir()
            baseline=Path(directory)/'manifest.json'; baseline.write_text(json.dumps(snapshot(root)))
            with redirect_stdout(io.StringIO()):
                self.assertEqual(main(['verify',str(root),'--manifest',str(baseline)]),0)
                (root/'new').write_text('x')
                self.assertEqual(main(['verify',str(root),'--manifest',str(baseline)]),1)
