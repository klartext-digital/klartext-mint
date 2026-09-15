#!/usr/bin/env python3
"""Publish checked output to gh-pages without changing source files or forcing Git."""
from pathlib import Path
import shutil, subprocess, sys, tempfile

ROOT = Path(__file__).resolve().parents[1]

def run(*args, cwd=ROOT, capture=False):
    return subprocess.run(args, cwd=cwd, check=True, text=True,
                          stdout=subprocess.PIPE if capture else None)

run(sys.executable, 'scripts/build.py')
run(sys.executable, 'scripts/check.py')
remote = run('git', 'remote', 'get-url', 'origin', capture=True).stdout.strip()
existing = run('git', 'ls-remote', '--heads', remote, 'gh-pages', capture=True).stdout.strip()
with tempfile.TemporaryDirectory(prefix='klartext-publish-') as temporary:
    checkout = Path(temporary) / 'site'
    if existing:
        run('git', 'clone', '--single-branch', '--branch', 'gh-pages', remote, str(checkout))
        # Only this newly created temporary checkout is cleaned; never the source repository.
        for path in checkout.iterdir():
            if path.name == '.git':
                continue
            if path.is_dir() and not path.is_symlink():
                shutil.rmtree(path)
            else:
                path.unlink()
    else:
        checkout.mkdir()
        run('git', 'init', '-b', 'gh-pages', cwd=checkout)
        run('git', 'remote', 'add', 'origin', remote, cwd=checkout)
    for path in (ROOT / '_site').iterdir():
        if path.is_dir():
            shutil.copytree(path, checkout / path.name)
        else:
            shutil.copy2(path, checkout / path.name)
    run('git', 'add', '--all', cwd=checkout)
    changed = subprocess.run(['git', 'diff', '--cached', '--quiet'], cwd=checkout).returncode
    if changed == 0:
        print('Published output already matches the checked build.')
    else:
        revision = run('git', 'rev-parse', '--short', 'HEAD', capture=True).stdout.strip()
        run('git', 'commit', '-m', 'Publish checked website from ' + revision, cwd=checkout)
        run('git', 'push', 'origin', 'HEAD:gh-pages', cwd=checkout)
        print('Published checked files to gh-pages. GitHub Pages must use gh-pages / as source.')
