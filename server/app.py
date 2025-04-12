#!/usr/bin/env python3
"""
Personality Test MCP Server
"""

import json
import logging
from typing import Dict, List, Optional, Any
from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
import uvicorn

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Personality Test MCP Server")

# Define models for MCP protocol
class MCPRequest(BaseModel):
    query: str
    context: Optional[Dict[str, Any]] = None

class MCPResponse(BaseModel):
    response: str
    context: Optional[Dict[str, Any]] = None

# Personality test questions
personality_questions = [
    # Extraversion (E) vs. Introversion (I)
    {"id": "EI1", "question": "You prefer spending time with others rather than alone.", "dimension": "EI"},
    {"id": "EI2", "question": "You often take initiative in social situations.", "dimension": "EI"},
    {"id": "EI3", "question": "You get energized from social gatherings.", "dimension": "EI"},
    {"id": "EI4", "question": "You enjoy being the center of attention.", "dimension": "EI"},
    {"id": "EI5", "question": "You prefer working in teams rather than independently.", "dimension": "EI"},
    
    # Sensing (S) vs. Intuition (N)
    {"id": "SN1", "question": "You focus more on details than the big picture.", "dimension": "SN"},
    {"id": "SN2", "question": "You prefer concrete facts over abstract theories.", "dimension": "SN"},
    {"id": "SN3", "question": "You trust experience more than intuition.", "dimension": "SN"},
    {"id": "SN4", "question": "You prefer practical solutions over innovative ideas.", "dimension": "SN"},
    {"id": "SN5", "question": "You focus more on present realities than future possibilities.", "dimension": "SN"},
    
    # Thinking (T) vs. Feeling (F)
    {"id": "TF1", "question": "You make decisions based on logic rather than feelings.", "dimension": "TF"},
    {"id": "TF2", "question": "You value objective truth over social harmony.", "dimension": "TF"},
    {"id": "TF3", "question": "You find it easy to criticize others when necessary.", "dimension": "TF"},
    {"id": "TF4", "question": "You prioritize efficiency over people's feelings.", "dimension": "TF"},
    {"id": "TF5", "question": "You prefer honest feedback over tactful communication.", "dimension": "TF"},
    
    # Judging (J) vs. Perceiving (P)
    {"id": "JP1", "question": "You prefer having a detailed plan rather than being spontaneous.", "dimension": "JP"},
    {"id": "JP2", "question": "You like to have things decided and settled.", "dimension": "JP"},
    {"id": "JP3", "question": "You prefer structure and order over flexibility.", "dimension": "JP"},
    {"id": "JP4", "question": "You tend to complete tasks well ahead of deadlines.", "dimension": "JP"},
    {"id": "JP5", "question": "You prefer environments that are neat and organized.", "dimension": "JP"}
]

# Personality type descriptions
personality_descriptions = {
    "ISTJ": "Quiet, serious, practical, and dependable. Values traditions and loyalty.",
    "ISFJ": "Quiet, friendly, responsible, and conscientious. Committed to meeting obligations.",
    "INFJ": "Seeks meaning and connection. Insightful about others with strong values.",
    "INTJ": "Independent, analytical, and determined. High standards and original thinking.",
    "ISTP": "Tolerant, flexible problem-solver. Interested in how things work.",
    "ISFP": "Quiet, friendly, sensitive, and kind. Enjoys the present moment.",
    "INFP": "Idealistic, loyal, and adaptable. Cares deeply about personal values.",
    "INTP": "Logical, original thinker. Interested in ideas and theoretical concepts.",
    "ESTP": "Flexible, tolerant, and spontaneous. Focuses on immediate results.",
    "ESFP": "Outgoing, friendly, and accepting. Enjoys making things fun for others.",
    "ENFP": "Enthusiastic, creative, and spontaneous. Sees possibilities and connections.",
    "ENTP": "Quick, ingenious, and stimulating. Enjoys new challenges.",
    "ESTJ": "Practical, realistic, and decisive. Organized and quick to implement decisions.",
    "ESFJ": "Warmhearted, conscientious, and cooperative. Seeks harmony and values traditions.",
    "ENFJ": "Warm, empathetic, responsive, and responsible. Attuned to others' needs.",
    "ENTJ": "Frank, decisive, and assumes leadership easily. Driven to organize and implement."
}

# Session storage for ongoing tests
active_sessions = {}

@app.post("/mcp", response_model=MCPResponse)
async def process_mcp_request(request: MCPRequest):
    """Process MCP requests for personality testing"""
    query = request.query.lower()
    context = request.context or {}
    session_id = context.get("session_id", "default")
    
    # Initialize session if it doesn't exist
    if session_id not in active_sessions:
        active_sessions[session_id] = {
            "current_question": 0,
            "answers": {},
            "completed": False,
            "personality_type": None
        }
    
    session = active_sessions[session_id]
    
    # Handle different query types
    if "start test" in query or "take personality test" in query:
        return start_test(session_id)
    elif "answer:" in query and not session["completed"]:
        # Extract answer (1-5) from query
        try:
            answer = int(query.split("answer:")[1].strip())
            if 1 <= answer <= 5:
                return process_answer(session_id, answer)
            else:
                return MCPResponse(
                    response="Please provide an answer between 1 (Strongly Disagree) and 5 (Strongly Agree).",
                    context={"session_id": session_id}
                )
        except (ValueError, IndexError):
            return MCPResponse(
                response="I couldn't understand your answer. Please respond with 'answer: X' where X is a number from 1-5.",
                context={"session_id": session_id}
            )
    elif "results" in query and session["completed"]:
        return get_results(session_id)
    else:
        # Default response
        if session["completed"]:
            return MCPResponse(
                response="Your personality test is complete. Ask for 'results' to see your personality type.",
                context={"session_id": session_id}
            )
        elif session["current_question"] > 0:
            current_q = personality_questions[session["current_question"] - 1]
            return MCPResponse(
                response=f"Please answer the current question: {current_q['question']} (1-5, where 1=Strongly Disagree, 5=Strongly Agree)",
                context={"session_id": session_id, "current_question": session["current_question"]}
            )
        else:
            return MCPResponse(
                response="Welcome to the Personality Test. Type 'start test' to begin.",
                context={"session_id": session_id}
            )

def start_test(session_id: str) -> MCPResponse:
    """Start a new personality test"""
    active_sessions[session_id] = {
        "current_question": 1,
        "answers": {},
        "completed": False,
        "personality_type": None
    }
    
    first_question = personality_questions[0]
    return MCPResponse(
        response=f"Let's start your personality test. For each statement, respond with a number from 1-5:\n"
                f"1 = Strongly Disagree\n2 = Disagree\n3 = Neutral\n4 = Agree\n5 = Strongly Agree\n\n"
                f"Question 1: {first_question['question']}\n\n"
                f"Respond with 'answer: X' where X is your rating.",
        context={"session_id": session_id, "current_question": 1, "total_questions": len(personality_questions)}
    )

def process_answer(session_id: str, answer: int) -> MCPResponse:
    """Process an answer and return the next question"""
    session = active_sessions[session_id]
    current_idx = session["current_question"] - 1
    
    # Store the answer
    current_question = personality_questions[current_idx]
    session["answers"][current_question["id"]] = answer
    
    # Move to next question
    session["current_question"] += 1
    
    # Check if test is complete
    if session["current_question"] > len(personality_questions):
        session["completed"] = True
        session["personality_type"] = calculate_personality_type(session["answers"])
        return MCPResponse(
            response="Thank you for completing the test! Type 'results' to see your personality type.",
            context={"session_id": session_id, "completed": True}
        )
    
    # Return next question
    next_question = personality_questions[session["current_question"] - 1]
    return MCPResponse(
        response=f"Question {session['current_question']}/{len(personality_questions)}: {next_question['question']}\n\n"
                f"(1=Strongly Disagree, 5=Strongly Agree)",
        context={
            "session_id": session_id, 
            "current_question": session["current_question"],
            "total_questions": len(personality_questions),
            "progress": f"{session['current_question']}/{len(personality_questions)}"
        }
    )

def calculate_personality_type(answers: Dict[str, int]) -> str:
    """Calculate MBTI personality type based on answers"""
    # Initialize scores for each dimension
    scores = {
        "EI": 0,  # Positive = E, Negative = I
        "SN": 0,  # Positive = S, Negative = N
        "TF": 0,  # Positive = T, Negative = F
        "JP": 0,  # Positive = J, Negative = P
    }
    
    # Calculate scores
    for question_id, answer in answers.items():
        dimension = next((q["dimension"] for q in personality_questions if q["id"] == question_id), None)
        if dimension:
            # Convert 1-5 scale to -2 to +2 scale
            adjusted_score = answer - 3
            scores[dimension] += adjusted_score
    
    # Determine type
    personality_type = ""
    personality_type += "E" if scores["EI"] >= 0 else "I"
    personality_type += "S" if scores["SN"] >= 0 else "N"
    personality_type += "T" if scores["TF"] >= 0 else "F"
    personality_type += "J" if scores["JP"] >= 0 else "P"
    
    return personality_type

def get_results(session_id: str) -> MCPResponse:
    """Return personality test results"""
    session = active_sessions[session_id]
    if not session["completed"]:
        return MCPResponse(
            response="You haven't completed the test yet.",
            context={"session_id": session_id}
        )
    
    personality_type = session["personality_type"]
    description = personality_descriptions.get(personality_type, "No description available.")
    
    return MCPResponse(
        response=f"Your personality type is: {personality_type}\n\n{description}",
        context={
            "session_id": session_id,
            "personality_type": personality_type,
            "description": description
        }
    )

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
