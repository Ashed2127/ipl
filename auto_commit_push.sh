#!/bin/bash

cd /home/ashed/Downloads/ipl_lang

echo "Starting auto-commit and push script (every 5 seconds)..."
echo "Press Ctrl+C to stop"

while true; do
    # Check if there are any changes
    if ! git diff --quiet || ! git diff --cached --quiet || [ -n "$(git ls-files --others --exclude-standard)" ]; then
        echo "[$(date)] Changes detected, committing and pushing..."
        
        # Get changed files
        CHANGED_FILES=$(git diff --name-only && git diff --cached --name-only && git ls-files --others --exclude-standard)
        
        # Generate commit message based on what changed
        COMMIT_MSG="Auto-commit: Update "
        
        # Count changed files
        FILE_COUNT=$(echo "$CHANGED_FILES" | wc -l)
        
        if [ "$FILE_COUNT" -eq 1 ]; then
            COMMIT_MSG+="file: $(echo "$CHANGED_FILES" | head -1)"
        else
            COMMIT_MSG+="$FILE_COUNT files: $(echo "$CHANGED_FILES" | head -5 | tr '\n' ', ')"
            if [ "$FILE_COUNT" -gt 5 ]; then
                COMMIT_MSG+=" and $((FILE_COUNT - 5)) more"
            fi
        fi
        
        # Add all changes
        git add -A
        
        # Commit with descriptive message
        git commit -m "$COMMIT_MSG

Generated with [Devin](https://devin.ai)

Co-Authored-By: Devin <158243242+devin-ai-integration[bot]@users.noreply.github.com>"
        
        # Push to remote
        git push
        
        echo "[$(date)] Committed and pushed successfully: $COMMIT_MSG"
    fi
    
    sleep 5
done
