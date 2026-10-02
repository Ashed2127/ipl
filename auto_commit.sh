#!/bin/bash
# Auto-commit and push script for IPL repository
# This script monitors file changes and automatically commits and pushes them

set -e

REPO_DIR="/home/ashed/Downloads/ipl_lang"
COMMIT_MESSAGE="Auto-commit: $(date '+%Y-%m-%d %H:%M:%S')"

cd "$REPO_DIR"

# Function to commit and push changes
commit_and_push() {
    # Check if there are changes
    if git diff --quiet && git diff --cached --quiet; then
        echo "No changes to commit"
        return
    fi

    # Add all changes
    git add -A

    # Commit with timestamp
    git commit -m "$COMMIT_MESSAGE

Generated with [Devin](https://devin.ai)

Co-Authored-By: Devin <158243242+devin-ai-integration[bot]@users.noreply.github.com>"

    # Push to remote
    git push origin $(git rev-parse --abbrev-ref HEAD)

    echo "✅ Changes committed and pushed: $COMMIT_MESSAGE"
}

# Run commit and push
commit_and_push
