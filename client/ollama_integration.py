#!/usr/bin/env python3
"""
Ollama Integration for Personality Test MCP
"""

import json
import requests
import argparse
from typing import Dict, Any, Optional
from mcp_client import PersonalityTestClient

class OllamaPersonalityIntegration:
    """
    Integrates personality test results with Ollama for personalized interactions
    """
    
    def __init__(self, ollama_url: str = "http://localhost:11434", model: str = "llama3"):
        self.ollama_url = ollama_url
        self.model = model
        self.personality_client = PersonalityTestClient()
        self.personality_type = None
        self.personality_description = None
    
    def run_personality_test(self):
        """Run the personality test and store the results"""
        print("Starting personality test to personalize your Ollama experience...")
        
        # Start the test
        print(self.personality_client.start_test())
        
        # Process questions until complete
        while "completed" not in self.personality_client.context or not self.personality_client.context["completed"]:
            try:
                answer = int(input("\nYour answer (1-5): "))
                if 1 <= answer <= 5:
                    response = self.personality_client.answer_question(answer)
                    print(f"\n{response}")
                else:
                    print("\nPlease enter a number between 1 and 5.")
            except ValueError:
                print("\nPlease enter a valid number.")
        
        # Get results
        results = self.personality_client.get_results()
        print("\n" + "=" * 60)
        print("Test Complete!")
        print("=" * 60)
        print(results)
        print("=" * 60)
        
        # Store personality information
        self.personality_type = self.personality_client.context.get("personality_type")
        self.personality_description = self.personality_client.context.get("description")
        
        return self.personality_type
    
    def generate_personality_system_prompt(self) -> str:
        """Generate a system prompt for Ollama based on personality type"""
        if not self.personality_type:
            return "You are a helpful AI assistant."
        
        # Create personalized system prompts based on personality type
        prompts = {
            # Analysts (NT)
            "INTJ": "You are communicating with an INTJ personality type. Be logical, direct, and efficient. Focus on concepts and ideas rather than small talk. Provide well-reasoned arguments and avoid emotional appeals. Respect their independence and offer insightful perspectives.",
            "INTP": "You are communicating with an INTP personality type. Engage with complex ideas and theoretical concepts. Be logical and precise in your explanations. Avoid social niceties and get straight to the intellectual content. Respect their need to question and analyze everything.",
            "ENTJ": "You are communicating with an ENTJ personality type. Be direct, efficient, and focused on results. Present information in a structured way with clear action items. Acknowledge their leadership qualities and provide strategic insights. Avoid being overly emotional or indecisive.",
            "ENTP": "You are communicating with an ENTP personality type. Engage with innovative ideas and be open to debate. Present multiple perspectives and possibilities. Use humor and wit when appropriate. Avoid rigid thinking or excessive detail without context.",
            
            # Diplomats (NF)
            "INFJ": "You are communicating with an INFJ personality type. Connect ideas to values and human impact. Be authentic and thoughtful in your responses. Acknowledge emotions and provide depth rather than surface-level answers. Respect their need for meaning and purpose.",
            "INFP": "You are communicating with an INFP personality type. Be gentle and authentic in your communication. Connect to values and personal meaning. Respect their individuality and avoid rigid structures. Acknowledge emotions and provide supportive, thoughtful responses.",
            "ENFJ": "You are communicating with an ENFJ personality type. Be warm and personable while still providing substance. Connect ideas to people and values. Acknowledge their supportive nature and leadership qualities. Provide positive reinforcement when appropriate.",
            "ENFP": "You are communicating with an ENFP personality type. Be enthusiastic and open to possibilities. Connect ideas in creative ways and avoid overly rigid structures. Use humor and warmth in your communication. Acknowledge their creativity and provide novel perspectives.",
            
            # Sentinels (SJ)
            "ISTJ": "You are communicating with an ISTJ personality type. Be clear, concise, and practical. Provide detailed, factual information with logical organization. Respect traditions and established methods. Avoid abstract theories without practical applications.",
            "ISFJ": "You are communicating with an ISFJ personality type. Be warm but practical in your communication. Respect traditions and provide detailed information. Acknowledge their helpful nature and desire for harmony. Be reliable and consistent in your responses.",
            "ESTJ": "You are communicating with an ESTJ personality type. Be direct, practical, and focused on results. Provide clear structure and actionable steps. Respect established procedures and be straightforward in your communication. Avoid ambiguity or excessive theorizing.",
            "ESFJ": "You are communicating with an ESFJ personality type. Be warm and considerate while providing practical information. Acknowledge social harmony and community values. Be specific and concrete rather than abstract. Provide supportive and structured responses.",
            
            # Explorers (SP)
            "ISTP": "You are communicating with an ISTP personality type. Be concise and practical. Focus on how things work and provide technical details when relevant. Respect their independence and problem-solving abilities. Avoid unnecessary social niceties or emotional content.",
            "ISFP": "You are communicating with an ISFP personality type. Be gentle and authentic in your communication. Respect their values and artistic sensibilities. Provide practical information with sensitivity. Avoid being pushy or overly structured in your approach.",
            "ESTP": "You are communicating with an ESTP personality type. Be direct and action-oriented. Focus on immediate results and practical applications. Use energetic language and get to the point quickly. Avoid abstract theories without clear applications.",
            "ESFP": "You are communicating with an ESFP personality type. Be friendly and enthusiastic. Focus on practical matters with a positive tone. Acknowledge their social nature and provide options rather than rigid structures. Use engaging language and concrete examples."
        }
        
        base_prompt = f"You are a helpful AI assistant communicating with someone who has a {self.personality_type} personality type. {self.personality_description}"
        
        return prompts.get(self.personality_type, base_prompt)
    
    def chat_with_ollama(self):
        """Start a chat session with Ollama using personality-tailored prompts"""
        if not self.personality_type:
            print("Please run a personality test first with .run_personality_test()")
            return
        
        system_prompt = self.generate_personality_system_prompt()
        
        print(f"\nStarting personalized chat for {self.personality_type} personality type...")
        print("Type 'exit' to end the conversation.\n")
        
        messages = [{"role": "system", "content": system_prompt}]
        
        while True:
            user_input = input("\nYou: ")
            if user_input.lower() == 'exit':
                break
                
            messages.append({"role": "user", "content": user_input})
            
            try:
                response = requests.post(
                    f"{self.ollama_url}/api/chat",
                    json={
                        "model": self.model,
                        "messages": messages,
                        "stream": False
                    }
                )
                response.raise_for_status()
                result = response.json()
                assistant_message = result["message"]["content"]
                
                print(f"\nAssistant: {assistant_message}")
                
                messages.append({"role": "assistant", "content": assistant_message})
                
            except requests.exceptions.RequestException as e:
                print(f"Error communicating with Ollama: {e}")
                break

def main():
    """Main function to run the Ollama integration"""
    parser = argparse.ArgumentParser(description="Personality Test Ollama Integration")
    parser.add_argument("--ollama", default="http://localhost:11434", help="Ollama API URL")
    parser.add_argument("--model", default="llama3", help="Ollama model to use")
    args = parser.parse_args()
    
    integration = OllamaPersonalityIntegration(ollama_url=args.ollama, model=args.model)
    integration.run_personality_test()
    integration.chat_with_ollama()

if __name__ == "__main__":
    main()
