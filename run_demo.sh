#!/bin/bash

# Run the Personality Test MCP Demo

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Python 3 is required but not installed. Please install Python 3 and try again."
    exit 1
fi

# Create and activate virtual environment
echo "Setting up virtual environment..."
python3 -m venv venv
source venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Start the server in the background
echo "Starting MCP server..."
cd server
python3 app.py &
SERVER_PID=$!

# Wait for server to start
echo "Waiting for server to start..."
sleep 3

# Check if Ollama is installed and running
if command -v ollama &> /dev/null; then
    echo "Checking Ollama status..."
    if curl -s http://localhost:11434/api/version &> /dev/null; then
        echo "Ollama is running. Starting personality test with Ollama integration..."
        cd ../client
        python3 ollama_integration.py
    else
        echo "Ollama is installed but not running. Starting basic personality test client..."
        cd ../client
        python3 mcp_client.py
    fi
else
    echo "Ollama not detected. Starting basic personality test client..."
    cd ../client
    python3 mcp_client.py
fi

# Clean up
echo "Stopping server..."
kill $SERVER_PID

echo "Demo complete!"
