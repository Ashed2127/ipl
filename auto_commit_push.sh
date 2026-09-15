#!/bin/bash

cd /home/ashed/Downloads/ipl_lang

echo "Starting auto-commit and push script (every 5 seconds)..."
echo "Press Ctrl+C to stop"

while true; do
    # Check if there are any changes
    if ! git diff --quiet || ! git diff --cached --quiet || [ -n "$(git ls-files --others --exclude-standard)" ]; then
        echo "[$(date)] Changes detected, committing and pushing..."
        
        # Add all changes
        git add -A
        
        # Commit with timestamp
        git commit -m "Auto-commit: $(date '+%Y-%m-%d %H:%M:%S')

Generated with [Devin](https://devin.ai)

Co-Authored-By: Devin <158243242+devin-ai-integration[bot]@users.noreply.github.com>"
        
        # Push to remote
        git push
        
        echo "[$(date)] Committed and pushed successfully"
    fi
    
    sleep 5
done
