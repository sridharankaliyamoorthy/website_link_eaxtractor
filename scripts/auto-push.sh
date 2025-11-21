#!/bin/bash

# Auto-push script with remote setup
# Usage: ./scripts/auto-push.sh [commit-message]

set -e

# Get current branch
CURRENT_BRANCH=$(git branch --show-current)

# Check if we're in a git repository
if ! git rev-parse --git-dir > /dev/null 2>&1; then
    echo "❌ Not a git repository. Run 'git init' first."
    exit 1
fi

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

# Check if remote exists
if ! git remote get-url origin &>/dev/null; then
    echo ""
    echo "⚠️  No remote repository configured!"
    echo ""
    read -p "Enter your GitHub repository URL: " REPO_URL
    
    if [ -z "$REPO_URL" ]; then
        echo "❌ Repository URL is required"
        exit 1
    fi
    
    # Validate URL format
    if [[ ! "$REPO_URL" =~ ^https://github.com/ ]] && [[ ! "$REPO_URL" =~ ^git@github.com: ]]; then
        echo "⚠️  Warning: URL doesn't look like a GitHub URL"
        read -p "Continue anyway? (y/n): " -n 1 -r
        echo ""
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            exit 1
        fi
    fi
    
    git remote add origin "$REPO_URL" 2>/dev/null || git remote set-url origin "$REPO_URL"
    echo "✅ Remote 'origin' set to: $REPO_URL"
fi

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

