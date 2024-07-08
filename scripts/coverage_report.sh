#!/usr/bin/env bash
set -euo pipefail

# Generate HTML coverage report from existing .coverage data
if [ -f .coverage ]; then
  coverage html -d coverage_html
  echo "HTML coverage generated at coverage_html/"
  exit 0
else
  echo ".coverage file not found; running pytest to generate coverage..."
  pytest --maxfail=1 --disable-warnings -q --cov=. --cov-report=html:coverage_html
  exit $?
fi
