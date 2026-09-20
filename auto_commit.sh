#!/bin/bash

while true; do
    # Check if there are any changes
    if [ -n "$(git status --porcelain)" ]; then
        # Add all changes
        git add .
        
        # Commit with timestamp
        git commit -m "Auto-commit: $(date '+%Y-%m-%d %H:%M:%S')"
        
        # Push to remote
        git push origin main
        
        echo "Auto-committed and pushed at $(date '+%Y-%m-%d %H:%M:%S')"
    fi
    
    # Wait for 5 seconds
    sleep 5
done
