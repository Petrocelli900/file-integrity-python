"""Create or compare SHA-256 file manifests without changing source files."""
import argparse
import hashlib
import json
import os
from pathlib import Path,PurePosixPath
import re
import sys

def snapshot(root):
    root=Path(root)
    if root.is_symlink() or not root.is_dir(): raise ValueError("Root must be a real directory")
    result={}
    for directory,dirs,files in os.walk(root,followlinks=False):
        for name in dirs+files:
            if (Path(directory)/name).is_symlink(): raise ValueError("Symbolic links are not supported")
        for name in sorted(files):
            path=Path(directory)/name
            if not path.is_file(): raise ValueError("Only regular files are supported")
            before=path.stat(); digest=hashlib.sha256()
            with path.open('rb') as stream:
                while block:=stream.read(1024*1024): digest.update(block)
            after=path.stat()
            if (before.st_size,before.st_mtime_ns,before.st_ino)!=(after.st_size,after.st_mtime_ns,after.st_ino):
                raise ValueError("File changed while hashing")
            result[path.relative_to(root).as_posix()]={'size':after.st_size,'sha256':digest.hexdigest()}
    return {'version':1,'files':dict(sorted(result.items()))}

def validate(manifest):
    if not isinstance(manifest,dict) or type(manifest.get('version')) is not int or manifest['version']!=1:
        raise ValueError("Unsupported manifest")
    files=manifest.get('files')
    if not isinstance(files,dict): raise ValueError("files must be an object")
    for name,record in files.items():
        if not isinstance(name,str) or not name or '\\' in name: raise ValueError("Invalid relative path")
        path=PurePosixPath(name)
        if path.is_absolute() or '..' in path.parts or name!=path.as_posix() or name=='.':
            raise ValueError("Invalid relative path")
        if not isinstance(record,dict) or type(record.get('size')) is not int or record['size']<0:
            raise ValueError("Invalid size")
        if not isinstance(record.get('sha256'),str) or re.fullmatch('[0-9a-f]{64}',record['sha256']) is None:
            raise ValueError("Invalid hash")
    return files

def compare(baseline,current):
    old=validate(baseline); new=validate(current)
    return {'added':sorted(new.keys()-old.keys()),'removed':sorted(old.keys()-new.keys()),
            'changed':sorted(name for name in old.keys() & new.keys() if old[name]!=new[name])}

def main(argv=None):
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('command',choices=['snapshot','verify']); parser.add_argument('root')
    parser.add_argument('--manifest')
    args=parser.parse_args(argv)
    if args.command=='verify' and not args.manifest: parser.error('verify requires --manifest')
    try:
        current=snapshot(args.root)
        if args.command=='snapshot': output=current; status=0
        else:
            with open(args.manifest,encoding='utf-8') as stream: baseline=json.load(stream)
            output=compare(baseline,current); status=int(any(output.values()))
    except (OSError,ValueError,TypeError) as error:
        print(str(error),file=sys.stderr); return 2
    print(json.dumps(output,ensure_ascii=False,indent=2)); return status

if __name__=='__main__': sys.exit(main())
