# Personality Test MCP Server

[![smithery badge](https://smithery.ai/badge/@devshark/personality-test-mcp)](https://smithery.ai/server/@devshark/personality-test-mcp)

This is a Model Context Protocol (MCP) implementation for personality testing. It allows AI models to administer personality tests, score responses, and provide personality type assessments.

## Features

- Administers a personality questionnaire to users
- Scores responses according to established personality frameworks
- Returns personality type and brief descriptions
- Integrates with Ollama for personalized AI interactions
- Allows users to go back and change previous answers

## Components

### Server

The MCP server handles:
- Serving personality test questions
- Processing and scoring user responses
- Determining personality types
- Storing user profiles (optional)

### Client

The client interface allows:
- Users to take the personality test
- Viewing results and personality descriptions
- Integration with Ollama for personalized interactions

## Personality Framework

This implementation uses a simplified version of the Myers-Briggs Type Indicator (MBTI) framework, which categorizes personalities along four dimensions:

1. **Extraversion (E) vs. Introversion (I)**: Where you focus your attention and get energy
2. **Sensing (S) vs. Intuition (N)**: How you take in information
3. **Thinking (T) vs. Feeling (F)**: How you make decisions
4. **Judging (J) vs. Perceiving (P)**: How you deal with the outer world

The combination of preferences results in 16 distinct personality types (e.g., INTJ, ESFP).

## Getting Started

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Ollama (optional, for personalized AI interactions)

### Installation and Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/model-context-protocols.git
   cd model-context-protocols/personality-test-mcp
   ```

2. Create and activate a virtual environment:
   ```bash
   python3 -m venv venv
   
   # On macOS/Linux
   source venv/bin/activate
   
   # On Windows
   venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Running the Server

1. Start the MCP server:
   ```bash
   cd server
   python app.py
   ```
   The server will start on http://localhost:8000

### Running the Client

1. In a new terminal, activate the virtual environment:
   ```bash
   cd personality-test-mcp
   source venv/bin/activate  # On macOS/Linux
   ```

2. Run the basic client:
   ```bash
   cd client
   python mcp_client.py
   ```

### Using Ollama Integration

If you have Ollama installed and running:

1. Make sure Ollama is running:
   ```bash
   ollama serve
   ```

2. Run the Ollama integration client:
   ```bash
   cd client
   python ollama_integration.py --model llama3
   ```
   You can replace `llama3` with any model you have available in Ollama.

### Using the Demo Script

For convenience, you can use the provided demo script:

1. Make the script executable:
   ```bash
   chmod +x run_demo.sh
   ```

2. Run the demo:
   ```bash
   ./run_demo.sh
   ```

This script will:
- Set up a virtual environment
- Install dependencies
- Start the server
- Run either the basic client or Ollama integration (if Ollama is detected)

## Docker Support

You can also run the server using Docker:

```bash
docker build -t personality-test-mcp .
docker run -p 8000:8000 personality-test-mcp
```

## Usage with AI Models

AI models can use this MCP to:
1. Administer personality tests to users
2. Retrieve personality profiles for personalized interactions
3. Adjust communication style based on personality preferences

## API Endpoints

- `POST /mcp`: Main MCP endpoint for personality test interactions
- `GET /health`: Health check endpoint

## License

This project is licensed under the [ISC license](LICENSE).

## Author

&copy; Anthony Lim
