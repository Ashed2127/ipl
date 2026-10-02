#!/bin/bash
# Watch files and auto-commit changes (polling version - no inotify-tools required)
# This version uses simple polling to detect changes

set -e

REPO_DIR="/home/ashed/Downloads/ipl_lang"
cd "$REPO_DIR"

echo "👀 Watching for file changes in $REPO_DIR (polling every 5 seconds)"
echo "Press Ctrl+C to stop"
echo ""

# Get initial state
LAST_COMMIT=$(git rev-parse HEAD)

while true; do
    sleep 5

    # Check if there are uncommitted changes (both staged and unstaged)
    if ! git diff --quiet || ! git diff --cached --quiet; then
        echo "📝 Changes detected at $(date '+%Y-%m-%d %H:%M:%S')"

        # Commit and push
        bash "$REPO_DIR/auto_commit.sh"

        # Update last commit
        LAST_COMMIT=$(git rev-parse HEAD)

        # Wait a bit to avoid rapid successive commits
        sleep 5
    fi
done
