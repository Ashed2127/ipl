#!/bin/bash

cd /home/ashed/Downloads/ipl_lang

echo "Starting auto-commit and push script (every 7 seconds)..."
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
            COMMIT_MSG="Add features: $(echo "$FEATURE_NAMES" | tr '\n' ', ' | sed 's/, $//')"
        fi
        
        # If no clear features found, analyze the content for meaningful changes
        if [ -z "$COMMIT_MSG" ]; then
            # Look for significant additions (long added lines, imports, security changes, etc.)
            SIGNIFICANT_ADDITIONS=$(echo "$DIFF_OUTPUT" | grep -E "^\+" | grep -v "^\+\+\+" | head -5)
            
            # Check for compiler-related changes
            if echo "$CHANGED_FILES" | grep -qi "compiler\|lexer\|parser\|ast"; then
                COMPILER_FILES=$(echo "$CHANGED_FILES" | grep -iE "compiler|lexer|parser|ast" | head -3)
                COMMIT_MSG="Update compiler components: $(echo "$COMPILER_FILES" | xargs -n1 basename | tr '\n' ', ' | sed 's/, $//')"
            # Check for runtime changes
            elif echo "$CHANGED_FILES" | grep -qi "runtime"; then
                COMMIT_MSG="Update runtime environment and execution engine"
            # Check for AI-related changes
            elif echo "$CHANGED_FILES" | grep -qi "ai\|hierarchical\|neural\|machine learning"; then
                AI_FILES=$(echo "$CHANGED_FILES" | grep -iE "ai|hierarchical|neural" | head -3)
                COMMIT_MSG="Update AI components: $(echo "$AI_FILES" | xargs -n1 basename | tr '\n' ', ' | sed 's/, $//')"
            # Check for security-related changes
            elif echo "$SIGNIFICANT_ADDITIONS" | grep -qi "security\|auth\|prompt\|injection\|vulnerability"; then
                COMMIT_MSG="Enhance security: AI prompt engineering and validation"
            # Check for test-related changes
            elif echo "$CHANGED_FILES" | grep -qi "test"; then
                TEST_FILES=$(echo "$CHANGED_FILES" | grep -i "test" | head -3)
                COMMIT_MSG="Update tests: $(echo "$TEST_FILES" | xargs -n1 basename | tr '\n' ', ' | sed 's/, $//')"
            # Check for documentation additions
            elif echo "$CHANGED_FILES" | grep -q "\.md$"; then
                NEW_DOCS=$(echo "$CHANGED_FILES" | grep "\.md$" | head -3)
                COMMIT_MSG="Add documentation: $(echo "$NEW_DOCS" | xargs -n1 basename | tr '\n' ', ' | sed 's/, $//')"
            # Check for configuration changes
            elif echo "$SIGNIFICANT_ADDITIONS" | grep -qi "config\|setting\|option"; then
                COMMIT_MSG="Update configuration and settings"
            # Check for import/library additions
            elif echo "$SIGNIFICANT_ADDITIONS" | grep -q "import\|from"; then
                COMMIT_MSG="Add imports and dependencies"
            # Check for type/structure changes
            elif echo "$SIGNIFICANT_ADDITIONS" | grep -qi "type\|class\|struct\|interface"; then
                COMMIT_MSG="Update type definitions and structures"
            # Check for bug fixes
            elif echo "$SIGNIFICANT_ADDITIONS" | grep -qi "fix\|bug\|error\|exception"; then
                COMMIT_MSG="Fix bugs and errors"
            # Check for performance improvements
            elif echo "$SIGNIFICANT_ADDITIONS" | grep -qi "performance\|optimize\|speed\|fast"; then
                COMMIT_MSG="Improve performance"
            # Check for refactoring
            elif echo "$SIGNIFICANT_ADDITIONS" | grep -qi "refactor\|clean\|simplify"; then
                COMMIT_MSG="Refactor code structure"
            # Default to file-based message
            else
                FILE_COUNT=$(echo "$CHANGED_FILES" | wc -l)
                if [ "$FILE_COUNT" -eq 1 ]; then
                    FILE_NAME=$(echo "$CHANGED_FILES" | head -1 | xargs basename)
                    COMMIT_MSG="Update $FILE_NAME"
                else
                    FILE_NAMES=$(echo "$CHANGED_FILES" | head -3 | xargs -n1 basename | tr '\n' ', ' | sed 's/, $//')
                    COMMIT_MSG="Update files: $FILE_NAMES"
                    if [ "$FILE_COUNT" -gt 3 ]; then
                        COMMIT_MSG+=" and more"
                    fi
                fi
            fi
        fi
        
        # Add all changes
        git add -A
        
        # Commit with descriptive message
        git commit -m "$COMMIT_MSG"
        
        # Push to remote
        git push
        
        echo "[$(date)] Committed and pushed successfully: $COMMIT_MSG"
    fi
    
    sleep 7
done
