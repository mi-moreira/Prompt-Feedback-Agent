#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

if [ ! -d "$repo_root/.githooks" ]; then
  mkdir -p "$repo_root/.githooks"
fi

# Ensure hook file exists
if [ ! -f "$repo_root/.githooks/prevent-commit-env" ]; then
  echo "ERROR: Hook file .githooks/prevent-commit-env not found. Create it first." >&2
  exit 2
fi

# Make hook executable
chmod +x "$repo_root/.githooks/prevent-commit-env"

# Configure git to use the hooks path
git -C "$repo_root" config core.hooksPath .githooks

echo "Git hooks installed. .githooks/prevent-commit-env is executable and core.hooksPath is set."
echo "To test: try staging a .env and committing (it should be blocked). If .env is in .gitignore you can force-add for testing:"
echo "  git add -f .env && git commit -m 'test'  # should be blocked by hook"
