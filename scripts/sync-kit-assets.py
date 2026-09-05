#!/usr/bin/env python3
"""Keep standalone plugin payloads derived from their shared source owners."""
import argparse
from pathlib import Path
import shutil

ROOT = Path(__file__).resolve().parents[1]

def assets():
    for host in ('codex', 'claude'):
        plugin = ROOT / host / 'plugins/semantic-memory'
        for name in ('semantic-memory-launch.sh', 'run-server-admin.sh'):
            yield ROOT / 'shared/scripts' / name, plugin / 'scripts' / name
    for host in ('codex', 'claude', 'hermes'):
        destination = ROOT / host
        if host != 'hermes': destination /= 'plugins/semantic-memory'
        yield ROOT / 'shared/skills/governed-memory/SKILL.md', destination / 'skills/governed-memory/SKILL.md'
        yield ROOT / 'shared/skills/memory-capture/SKILL.md', destination / 'skills/memory-capture/SKILL.md'

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    drift = []
    for source, target in assets():
        if args.check:
            if not target.is_file() or target.read_bytes() != source.read_bytes() or (target.stat().st_mode & 0o111) != (source.stat().st_mode & 0o111):
                drift.append(str(target.relative_to(ROOT)))
        else:
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source, target)
    if drift:
        parser.exit(1, 'Generated kit assets differ: ' + ', '.join(drift) + '\n')
    print('Kit assets match shared owners' if args.check else 'Kit assets synchronized')

if __name__ == '__main__': main()
