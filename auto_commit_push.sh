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
        
        # Generate commit message based on actual changes
        COMMIT_MSG=""
        
        # Analyze changes to extract feature information
        DIFF_OUTPUT=$(git diff && git diff --cached)
        
        # Look for actual function/class definitions (not variable assignments)
        ADDED_FEATURES=$(echo "$DIFF_OUTPUT" | grep -E "^\+ *def [a-zA-Z_]|^\+ *class [a-zA-Z_]|^\+ *function [a-zA-Z_]" | grep -v "=" | sed 's/^[+] *//' | head -3)
        
        if [ -n "$ADDED_FEATURES" ]; then
            # Clean up the feature names to get just the function/class names
            FEATURE_NAMES=$(echo "$ADDED_FEATURES" | sed -E 's/.*def ([a-zA-Z_][a-zA-Z0-9_]*).*/\1/; s/.*class ([a-zA-Z_][a-zA-Z0-9_]*).*/\1/; s/.*function ([a-zA-Z_][a-zA-Z0-9_]*).*/\1/' | head -3)
            COMMIT_MSG="Add: $(echo "$FEATURE_NAMES" | tr '\n' ', ' | sed 's/, $//')"
        fi
        
        # If no clear features found, use file-based message
        if [ -z "$COMMIT_MSG" ]; then
            FILE_COUNT=$(echo "$CHANGED_FILES" | wc -l)
            if [ "$FILE_COUNT" -eq 1 ]; then
                COMMIT_MSG="Update $(echo "$CHANGED_FILES" | head -1)"
            else
                COMMIT_MSG="Update $FILE_COUNT files: $(echo "$CHANGED_FILES" | head -3 | tr '\n' ', ' | sed 's/, $//')"
                if [ "$FILE_COUNT" -gt 3 ]; then
                    COMMIT_MSG+=" and more"
                fi
            fi
        fi
        
        # Add all changes
        git add -A
        
        # Commit with descriptive message
        git commit -m "$COMMIT_MSG"
        
        # Push to remote
        git push
        
        echo "[$(date)] Committed and pushed successfully"
    fi
    
    sleep 5
done
