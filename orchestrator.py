import os
from datetime import datetime
from dotenv import load_dotenv
from smolagents import CodeAgent, OpenAIServerModel

# Import the custom ETL tool we built in the previous step
from email_tool import fetch_unread_newsletters

# 1. Load environment variables (your App Password)
load_dotenv()

# 2. Connect to the local AMD-powered LLM via Ollama
model = OpenAIServerModel(
    model_id="qwen2.5-coder:7b", 
    api_base="http://localhost:11434/v1", 
    api_key="ollama" 
)

# 3. Initialize the Agent and equip it with the "hands" to read email
# We set add_base_tools=False to save context window space, as it doesn't need web search here
agent = CodeAgent(
    tools=[fetch_unread_newsletters], 
    model=model, 
    add_base_tools=False 
)

# 4. Define the Agent's specific task and prompt logic
task_prompt = """
You are an expert AI Data Analyst and Newsletter Editor.
Perform the following steps:
1. Use the `fetch_unread_newsletters` tool to read the latest emails from the inbox. 
2. Analyze the text. Ignore any purely promotional material or administrative footers.
3. For each relevant newsletter, generate a clean, engaging summary with 3-4 bullet points highlighting the most important facts or insights.
4. Format your final output so it reads like a daily briefing script, as this will eventually be fed into a Text-to-Speech engine. 
"""

print("Agent is connecting to the inbox and thinking... (This may take a minute depending on email length)")

# Execute the agentic loop
response = str(agent.run(task_prompt))

# 5. Save the output to a local Markdown file for your records
timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M")
filename = f"digest_{timestamp}.md"

with open(filename, "w", encoding="utf-8") as f:
    f.write(response)

print(f"\n--- Orchestration Complete! ---")
print(f"Digest successfully saved to: {filename}")
print("\n--- Digest Preview ---")
print(response)