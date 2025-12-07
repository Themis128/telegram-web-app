#!/bin/bash

# Bash script to start the Telegram Web App

echo "Starting Telegram Web Application..."

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not installed"
    exit 1
fi

echo "Python found: $(python3 --version)"

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo "Warning: .env file not found. Creating from env.example..."
    cp env.example .env
    echo "Please edit .env and add your Telegram credentials"
fi

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Start the application
echo "Starting application on http://localhost:8000"
echo "Press Ctrl+C to stop"
python3 app.py
