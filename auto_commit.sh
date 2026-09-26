#!/bin/bash

# Auto-commit and push script
# Run this on a schedule (e.g., using cron or a loop)

cd /home/ashed/Downloads/ipl_lang

# Check if there are changes
if git diff --quiet && git diff --cached --quiet; then
    echo "No changes to commit"
    exit 0
fi

# Add all changes
git add .

# Commit with timestamp
git commit -m "Auto-commit: $(date '+%Y-%m-%d %H:%M:%S')"

# Push to GitHub
git push origin main

echo "Auto-commit and push completed at $(date '+%Y-%m-%d %H:%M:%S')"
