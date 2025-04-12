#!/bin/bash

# Run tests with MCP Inspector

# Check if MCP Inspector is installed
if ! command -v mcp-inspector &> /dev/null; then
    echo "MCP Inspector is not installed. Installing..."
    npm install -g mcp-inspector
fi

# Start the MCP server in the background
echo "Starting Personality Test MCP server..."
cd server
python app.py &
SERVER_PID=$!

# Wait for server to start
echo "Waiting for server to start..."
sleep 3

# Run the MCP Inspector
echo "Running MCP Inspector..."
mcp-inspector --config ../mcp_inspector_config.json

# Alternative: Run the Python test script
echo "Running Python test script..."
cd ..
python test_with_inspector.py

# Clean up
echo "Stopping server..."
kill $SERVER_PID

echo "Test complete!"
