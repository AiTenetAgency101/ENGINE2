#!/usr/bin/env bash
set -e
echo "=== HEALTH CHECK START ==="
echo "Repo root:"
pwd
echo "Listing files:"
ls -R .
echo "Bash version:"
bash --version
echo "=== HEALTH CHECK COMPLETE ==="
