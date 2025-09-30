#!/bin/bash

# Claude Optimization Suite - Setup Script
# התקנה ראשונית של הסביבה

set -e  # Exit on error

echo "🚀 Starting Claude Optimization Suite Setup..."

# Check Python version
echo "📦 Checking Python version..."
python3 --version

# Create virtual environment
echo "🔧 Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo "✅ Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "⬆️  Upgrading pip..."
pip install --upgrade pip

# Install requirements
echo "📥 Installing Python dependencies..."
pip install -r requirements.txt

# Create necessary directories
echo "📁 Creating directories..."
mkdir -p logs
mkdir -p backups
mkdir -p data
mkdir -p outputs

# Copy environment file if it doesn't exist
if [ ! -f .env ]; then
    echo "📝 Creating .env file from template..."
    cp .env.example .env
    echo "⚠️  Please edit .env and add your API keys!"
else
    echo "✅ .env file already exists"
fi

# Make scripts executable
echo "🔐 Setting permissions..."
chmod +x setup.sh
chmod +x main.py
chmod +x claude_optimizer.py

echo ""
echo "✅ Setup completed successfully!"
echo ""
echo "Next steps:"
echo "1. Edit .env file and add your CLAUDE_API_KEY"
echo "2. Activate virtual environment: source venv/bin/activate"
echo "3. Run the application: python main.py"
echo ""
echo "For more information, see README.md"