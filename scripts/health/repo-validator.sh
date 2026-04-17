#!/usr/bin/env bash
set -e

echo "=== ENGINE2 REPO VALIDATOR ==="

echo "Checking required folders..."
for d in engine engine_core modules scripts; do
  if [ ! -d "$d" ]; then
    echo "Missing folder: $d"
  fi
done

echo "Checking Python files..."
find . -name "*.py" | wc -l

echo "Checking YAML validity..."
find . -name "*.yml" -exec yamllint {} \; || true

echo "=== VALIDATION COMPLETE ==="
