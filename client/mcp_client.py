#!/usr/bin/env python3
"""
Personality Test MCP Client
"""

import json
import uuid
import requests
import argparse
from typing import Dict, Any, Optional

class PersonalityTestClient:
    """Client for interacting with the Personality Test MCP Server"""
    
    def __init__(self, server_url: str = "http://localhost:8000"):
        self.server_url = server_url
        self.session_id = str(uuid.uuid4())
        self.context = {"session_id": self.session_id}
    
    def send_query(self, query: str) -> Dict[str, Any]:
        """Send a query to the MCP server"""
        payload = {
            "query": query,
            "context": self.context
        }
        
        try:
            response = requests.post(f"{self.server_url}/mcp", json=payload)
            response.raise_for_status()
            result = response.json()
            
            # Update context with server response
            if result.get("context"):
                self.context.update(result["context"])
                
            return result
        except requests.exceptions.RequestException as e:
            print(f"Error communicating with MCP server: {e}")
            return {"response": "Error: Could not connect to MCP server", "context": self.context}
    
    def start_test(self) -> str:
        """Start the personality test"""
        result = self.send_query("start test")
        return result["response"]
    
    def answer_question(self, answer: int) -> str:
        """Submit an answer to the current question"""
        result = self.send_query(f"answer: {answer}")
        return result["response"]
    
    def get_results(self) -> str:
        """Get the personality test results"""
        result = self.send_query("results")
        return result["response"]
    
    def get_personality_type(self) -> Optional[str]:
        """Get just the personality type from the context"""
        return self.context.get("personality_type")

def interactive_test(client: PersonalityTestClient):
    """Run an interactive personality test in the terminal"""
    print("=" * 60)
    print("Personality Test MCP Client")
    print("=" * 60)
    
    # Start the test
    print(client.start_test())
    
    # Process questions until complete
    while "completed" not in client.context or not client.context["completed"]:
        try:
            answer = int(input("\nYour answer (1-5): "))
            if 1 <= answer <= 5:
                response = client.answer_question(answer)
                print(f"\n{response}")
            else:
                print("\nPlease enter a number between 1 and 5.")
        except ValueError:
            print("\nPlease enter a valid number.")
    
    # Show results
    print("\n" + "=" * 60)
    print("Test Complete!")
    print("=" * 60)
    print(client.get_results())
    print("=" * 60)

def main():
    """Main function to run the client"""
    parser = argparse.ArgumentParser(description="Personality Test MCP Client")
    parser.add_argument("--server", default="http://localhost:8000", help="MCP server URL")
    args = parser.parse_args()
    
    client = PersonalityTestClient(server_url=args.server)
    interactive_test(client)

if __name__ == "__main__":
    main()
