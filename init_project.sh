#!/bin/bash

# Exit immediately if a command exits with a non-zero status
set -e

echo "🚀 Starting project initialization..."

# 1. Check if requirements.txt exists
if [ ! -f "requirements.txt" ]; then
    echo "❌ Error: requirements.txt not found! Please create it first."
    exit 1
fi

# 2. Create virtual environment if it doesn't exist
if [ ! -d ".venv" ]; then
    echo "📦 Creating virtual environment (.venv)..."
    python3 -m venv .venv
else
    echo "ℹ️ Virtual environment (.venv) already exists."
fi

# 3. Activate virtual environment
echo "🔄 Activating virtual environment..."
source .venv/bin/activate

# 4. Upgrade pip and install requirements
echo "📥 Upgrading pip..."
pip install --upgrade pip

echo "📥 Installing dependencies from requirements.txt..."
pip install -r requirements.txt

echo "✅ Initialization complete! Virtual environment is ready."
echo "💡 To activate it in your current terminal, run: source .venv/bin/activate"
