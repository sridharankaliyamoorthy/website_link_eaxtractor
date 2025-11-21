#!/bin/bash

# Auto-push script with remote setup
# Usage: ./scripts/auto-push.sh [commit-message]

set -e

# Load utility functions
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/git-utils.sh" 2>/dev/null || {
    echo "⚠️  Warning: Could not load git-utils.sh"
}

# Get current branch
CURRENT_BRANCH=$(git branch --show-current)

# Check if we're in a git repository
if ! git rev-parse --git-dir > /dev/null 2>&1; then
    echo "❌ Not a git repository. Run 'git init' first."
    exit 1
fi

# Show current repo status
echo "🔍 Checking repository configuration..."
show_repo_status 2>/dev/null || echo ""

# Check if there are changes to commit
if [ -n "$(git status --porcelain)" ]; then
    echo "📝 Staging all changes..."
    git add -A
    
    # Get commit message
    if [ -n "$1" ]; then
        COMMIT_MSG="$1"
    else
        read -p "💬 Enter commit message: " COMMIT_MSG
        if [ -z "$COMMIT_MSG" ]; then
            echo "❌ Commit message cannot be empty"
            exit 1
        fi
    fi
    
    echo "💾 Committing changes..."
    git commit -m "$COMMIT_MSG"
fi

# Check and setup repository URL (only prompts if not found)
REPO_URL=$(check_and_setup_repo)
if [ $? -ne 0 ] || [ -z "$REPO_URL" ]; then
    echo "❌ Failed to get repository URL"
    exit 1
fi

# If we got here, repo URL is set (either existing or newly configured)
echo "✅ Using repository: $REPO_URL"

# Push to remote
echo ""
echo "📤 Pushing to origin/$CURRENT_BRANCH..."
git push -u origin "$CURRENT_BRANCH" 2>&1

if [ $? -eq 0 ]; then
    echo "✅ Successfully pushed to remote!"
    echo "🔗 Repository: $(git remote get-url origin)"
else
    echo "❌ Push failed. Check your remote URL and permissions."
    exit 1
fi

