#!/bin/bash
set -e

# Post-merge setup script for Project Dungeon Keeper
# This project is Python + documentation. No build step or migrations required.
# Install/verify Python dependencies only.

echo "Running post-merge setup..."

# Install Python dependencies if requirements.txt exists
if [ -f "requirements.txt" ]; then
    pip install -r requirements.txt --quiet
fi

echo "Post-merge setup complete."
