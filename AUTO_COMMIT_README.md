# Auto-Commit and Push System

This repository is configured to automatically track changes, commit them, and push to GitHub.

## Components

### 1. Post-Commit Hook (.git/hooks/post-commit)
Automatically pushes to GitHub after every commit. This runs automatically whenever you make a commit.

### 2. auto_commit.sh
Manually commit and push all changes with a timestamp.

```bash
bash auto_commit.sh
```

### 3. watch_and_commit.sh
Continuously monitor the repository for changes and auto-commit/push them every 5 seconds.

```bash
# Start watching (runs in foreground)
bash watch_and_commit.sh

# Run in background
nohup bash watch_and_commit.sh > /tmp/watch_commit.log 2>&1 &
```

## Usage

### Quick Commit and Push
```bash
bash auto_commit.sh
```

### Continuous Monitoring
```bash
# Start in background
bash watch_and_commit.sh &

# Or with nohup to keep running after terminal closes
nohup bash watch_and_commit.sh > /tmp/watch_commit.log 2>&1 &

# Check if it's running
ps aux | grep watch_and_commit

# Stop it
pkill -f watch_and_commit
```

### Normal Git Workflow
The post-commit hook will automatically push after any commit:
```bash
git add .
git commit -m "Your message"
# Auto-push happens automatically here
```

## Configuration

- **Polling Interval**: 5 seconds (edit watch_and_commit.sh to change)
- **Commit Message**: Auto-generated with timestamp
- **Branch**: Automatically pushes to current branch

## Notes

- The watch script excludes `.git/`, `__pycache__/`, `.pyc`, `.log`, `venv/`, and `.venv/` directories
- Changes are committed with a timestamp in the format: "Auto-commit: YYYY-MM-DD HH:MM:SS"
- All commits include Devin co-author attribution
