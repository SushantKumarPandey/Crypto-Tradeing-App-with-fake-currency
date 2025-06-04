#!/bin/bash
set -e

echo "==> Installing tools..."
pip install flake8 black isort pytest > /dev/null

echo "==> Running linters..."
flake8 .
black --check .
isort --check-only .

echo "==> Running tests..."
pytest

echo "


