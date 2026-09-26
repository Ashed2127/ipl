#!/bin/bash

# Run auto-commit script on a loop
# WARNING: Running every 7 seconds is very aggressive and not recommended

INTERVAL=${1:-7}  # Default 7 seconds, or pass as argument

echo "Starting auto-commit every $INTERVAL seconds..."
echo "Press Ctrl+C to stop"

while true; do
    /home/ashed/Downloads/ipl_lang/auto_commit.sh
    sleep $INTERVAL
done
