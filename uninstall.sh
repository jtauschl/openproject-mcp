#!/usr/bin/env bash
# macOS / Linux — removes the local virtual environment.
# Your .mcp.json is left untouched.
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$ROOT_DIR"

rm -rf .venv .pytest_cache
find . -type d -name "__pycache__" -prune -exec rm -rf {} +
find . -type d -name "*.egg-info" -prune -exec rm -rf {} +

echo
echo "Local environment removed."
echo "Your .mcp.json was left untouched."
