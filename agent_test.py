import os
from dotenv import load_dotenv
from smolagents import CodeAgent, OpenAIServerModel

# 1. Load your secure environment variables (for later use)
load_dotenv()

# 2. Connect to your local AMD-powered model via Ollama's local server
# Ollama runs on port 11434 by default and mimics the OpenAI API structure
model = OpenAIServerModel(
    model_id="llama3.2:3b", # Replace with your specific local model name if different
    api_base="http://localhost:11434/v1", 
    api_key="ollama" # Ollama requires a dummy key, it doesn't validate it
)

# 3. Initialize the Agent
# We are using a CodeAgent, which writes Python code to solve problems
agent = CodeAgent(tools=[], model=model, add_base_tools=True)

# 4. Run a simple test prompt
print("Agent is thinking...")
response = agent.run("What is 10 multiplied by 5? Write a quick python calculation to find out.")

print("\n--- Final Answer ---")
print(response)