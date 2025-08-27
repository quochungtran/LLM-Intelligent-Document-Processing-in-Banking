#!/usr/bin/env bash
set -e

# Check argument
if [ $# -lt 1 ]; then
    echo "Usage: $0 <python_file_or_dir>"
    exit 1
fi

TARGET=$1

# Check if file or directory exists
if [ ! -e "$TARGET" ]; then
    echo "Error: $TARGET does not exist."
    exit 1
fi


echo "✨ Formatting code with black..."
black "$TARGET"

echo "🔍 Running pylint..."
pylint "$TARGET"


echo "✅ Code quality check and auto-fix completed!"
