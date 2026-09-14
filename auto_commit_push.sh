#!/bin/bash

while true; do
    # Check if there are any changes
    if git diff --quiet && git diff --cached --quiet && [ -z "$(git ls-files --others --exclude-standard)" ]; then
        echo "No changes detected at $(date)"
    else
        echo "Changes detected at $(date)"
        # Add all changes
        git add -A
        # Commit with timestamp
        git commit -m "Auto-commit at $(date '+%Y-%m-%d %H:%M:%S')" --no-verify
        # Push to origin
        git push origin main
        echo "Committed and pushed successfully"
    fi
    sleep 15
done
