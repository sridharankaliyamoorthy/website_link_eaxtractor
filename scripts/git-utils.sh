#!/bin/bash

# Git utility functions for repository management
# This script provides functions to check and manage git repository configuration

# Configuration file location
CONFIG_FILE=".git-repo-config"

# Function to get repository URL from various sources
get_repo_url() {
    local repo_url=""
    
    # 1. Check git remote (highest priority)
    if git rev-parse --git-dir > /dev/null 2>&1; then
        repo_url=$(git remote get-url origin 2>/dev/null)
        if [ -n "$repo_url" ]; then
            echo "$repo_url"
            return 0
        fi
    fi
    
    # 2. Check config file
    if [ -f "$CONFIG_FILE" ]; then
        repo_url=$(grep "^GIT_REPO_URL=" "$CONFIG_FILE" 2>/dev/null | cut -d'=' -f2- | tr -d '"' | tr -d "'" | xargs)
        if [ -n "$repo_url" ] && [ "$repo_url" != "" ]; then
            echo "$repo_url"
            return 0
        fi
    fi
    
    # 3. Check environment variable
    if [ -n "$GIT_REPO_URL" ]; then
        echo "$GIT_REPO_URL"
        return 0
    fi
    
    # 4. Check .env file (if exists)
    if [ -f ".env" ]; then
        repo_url=$(grep "^GIT_REPO_URL=" ".env" 2>/dev/null | cut -d'=' -f2- | tr -d '"' | tr -d "'" | xargs)
        if [ -n "$repo_url" ] && [ "$repo_url" != "" ]; then
            echo "$repo_url"
            return 0
        fi
    fi
    
    return 1
}

# Function to save repository URL
save_repo_url() {
    local repo_url="$1"
    
    if [ -z "$repo_url" ]; then
        return 1
    fi
    
    # Save to config file
    if [ -f "$CONFIG_FILE" ]; then
        # Update existing config
        if grep -q "^GIT_REPO_URL=" "$CONFIG_FILE" 2>/dev/null; then
            sed -i '' "s|^GIT_REPO_URL=.*|GIT_REPO_URL=$repo_url|" "$CONFIG_FILE" 2>/dev/null || \
            sed -i "s|^GIT_REPO_URL=.*|GIT_REPO_URL=$repo_url|" "$CONFIG_FILE"
        else
            echo "GIT_REPO_URL=$repo_url" >> "$CONFIG_FILE"
        fi
    else
        # Create new config file
        cat > "$CONFIG_FILE" << EOF
# Git Repository Configuration
# This file stores the GitHub repository URL to avoid repeated prompts
# Format: GIT_REPO_URL=https://github.com/username/repo.git

GIT_REPO_URL=$repo_url
EOF
    fi
    
    # Also set git remote if in a git repo
    if git rev-parse --git-dir > /dev/null 2>&1; then
        if ! git remote get-url origin &>/dev/null; then
            git remote add origin "$repo_url" 2>/dev/null
        else
            git remote set-url origin "$repo_url" 2>/dev/null
        fi
    fi
}

# Function to check and setup repository URL (with prompt if needed)
check_and_setup_repo() {
    local repo_url=$(get_repo_url)
    
    if [ -n "$repo_url" ]; then
        echo "$repo_url"
        return 0
    fi
    
    # No repo URL found, prompt user
    echo ""
    echo "⚠️  No GitHub repository URL found."
    echo "   Checking: git remote, config file, environment variables..."
    echo ""
    read -p "Enter your GitHub repository URL: " repo_url
    
    if [ -z "$repo_url" ]; then
        echo "❌ Repository URL is required"
        return 1
    fi
    
    # Validate URL format
    if [[ ! "$repo_url" =~ ^https://github.com/ ]] && [[ ! "$repo_url" =~ ^git@github.com: ]]; then
        echo "⚠️  Warning: URL doesn't look like a GitHub URL"
        read -p "Continue anyway? (y/n): " -n 1 -r
        echo ""
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            return 1
        fi
    fi
    
    # Save the URL
    save_repo_url "$repo_url"
    echo "✅ Repository URL saved: $repo_url"
    echo "   (Stored in $CONFIG_FILE and git remote)"
    
    echo "$repo_url"
    return 0
}

# Function to display current repo status
show_repo_status() {
    echo "📋 Repository Status:"
    echo ""
    
    local repo_url=$(get_repo_url)
    
    if [ -n "$repo_url" ]; then
        echo "✅ Repository URL: $repo_url"
        echo "   Source: "
        
        # Check where it came from
        if git remote get-url origin &>/dev/null 2>&1; then
            local git_remote=$(git remote get-url origin 2>/dev/null)
            if [ "$git_remote" = "$repo_url" ]; then
                echo "   - Git remote (origin)"
            fi
        fi
        
        if [ -f "$CONFIG_FILE" ] && grep -q "^GIT_REPO_URL=$repo_url" "$CONFIG_FILE" 2>/dev/null; then
            echo "   - Config file (.git-repo-config)"
        fi
        
        if [ -n "$GIT_REPO_URL" ] && [ "$GIT_REPO_URL" = "$repo_url" ]; then
            echo "   - Environment variable (GIT_REPO_URL)"
        fi
    else
        echo "❌ No repository URL configured"
        echo "   Run: ./scripts/auto-push.sh to set it up"
    fi
    echo ""
}

