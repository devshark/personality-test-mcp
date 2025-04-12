#!/usr/bin/env python3
"""
Test script for validating the Personality Test MCP with MCP Inspector
"""

import json
import argparse
import requests
from typing import Dict, Any, Optional

class MCPInspectorTest:
    """Test the Personality Test MCP with MCP Inspector"""
    
    def __init__(self, mcp_server_url: str = "http://localhost:8000", 
                 inspector_url: str = "http://localhost:8080"):
        self.mcp_server_url = mcp_server_url
        self.inspector_url = inspector_url
        self.session_id = "test-session-123"
        self.context = {"session_id": self.session_id}
    
    def send_to_inspector(self, query: str) -> Dict[str, Any]:
        """Send a query to the MCP Inspector"""
        payload = {
            "mcp_endpoint": f"{self.mcp_server_url}/mcp",
            "query": query,
            "context": self.context
        }
        
        try:
            response = requests.post(f"{self.inspector_url}/inspect", json=payload)
            response.raise_for_status()
            result = response.json()
            
            # Update context with server response
            if result.get("context"):
                self.context.update(result["context"])
                
            return result
        except requests.exceptions.RequestException as e:
            print(f"Error communicating with MCP Inspector: {e}")
            return {"error": f"Could not connect to MCP Inspector: {e}"}
    
    def send_direct_to_mcp(self, query: str) -> Dict[str, Any]:
        """Send a query directly to the MCP server"""
        payload = {
            "query": query,
            "context": self.context
        }
        
        try:
            response = requests.post(f"{self.mcp_server_url}/mcp", json=payload)
            response.raise_for_status()
            result = response.json()
            
            # Update context with server response
            if result.get("context"):
                self.context.update(result["context"])
                
            return result
        except requests.exceptions.RequestException as e:
            print(f"Error communicating with MCP server: {e}")
            return {"error": f"Could not connect to MCP server: {e}"}
    
    def run_test_sequence(self, use_inspector: bool = True):
        """Run a test sequence through the personality test"""
        send_func = self.send_to_inspector if use_inspector else self.send_direct_to_mcp
        
        print("=" * 60)
        print(f"Testing Personality Test MCP {'with Inspector' if use_inspector else 'directly'}")
        print("=" * 60)
        
        # Start the test
        result = send_func("start test")
        print(f"\nQuery: start test")
        print(f"Response: {result.get('response')}")
        print(f"Context: {json.dumps(result.get('context', {}), indent=2)}")
        
        # Answer a few questions
        for i in range(3):
            answer = 3  # Neutral answer for testing
            result = send_func(f"answer: {answer}")
            print(f"\nQuery: answer: {answer}")
            print(f"Response: {result.get('response')}")
            print(f"Context: {json.dumps(result.get('context', {}), indent=2)}")
        
        # Try going back
        result = send_func("back")
        print(f"\nQuery: back")
        print(f"Response: {result.get('response')}")
        print(f"Context: {json.dumps(result.get('context', {}), indent=2)}")
        
        # Answer with a different value
        result = send_func("answer: 5")
        print(f"\nQuery: answer: 5")
        print(f"Response: {result.get('response')}")
        print(f"Context: {json.dumps(result.get('context', {}), indent=2)}")
        
        print("\nTest sequence completed successfully!")

def main():
    """Main function to run the test"""
    parser = argparse.ArgumentParser(description="Test Personality Test MCP with MCP Inspector")
    parser.add_argument("--mcp", default="http://localhost:8000", help="MCP server URL")
    parser.add_argument("--inspector", default="http://localhost:8080", help="MCP Inspector URL")
    parser.add_argument("--direct", action="store_true", help="Test directly without Inspector")
    args = parser.parse_args()
    
    tester = MCPInspectorTest(mcp_server_url=args.mcp, inspector_url=args.inspector)
    tester.run_test_sequence(not args.direct)

if __name__ == "__main__":
    main()
