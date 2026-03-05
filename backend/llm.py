import os
from dotenv import load_dotenv

from langchain_huggingface import HuggingFaceEndpoint, ChatHuggingFace
from langchain_core.messages import SystemMessage, HumanMessage

load_dotenv()

hf_token = os.getenv("HUGGINGFACE_API_TOKEN")

# Initialize model
llm = HuggingFaceEndpoint(
    repo_id="meta-llama/Llama-3.1-8B-Instruct",
    huggingfacehub_api_token=hf_token,
    task="text-generation",
    max_new_tokens=20000,
    temperature=0.7
)

chat = ChatHuggingFace(llm=llm)

# System prompt
system_prompt = """
You are a relationship analysis assistant.

Based on the relationship scores, generate insights.

Return ONLY valid JSON in this format:

{
  "strength": "one key relationship strength",
  "focus_area": "one area that needs improvement",
  "suggestion": "one practical suggestion for the couple"
}

Keep responses short (max 20 words each).
Do not include explanations or extra text.
"""


def generate_relationship_advice(scores):

    user_prompt = f"""
Relationship scores:

Emotional Connection: {scores['emotional']}%
Communication: {scores['communication']}%
Trust: {scores['trust']}%
Conflict Resolution: {scores['conflict']}%
Relationship Satisfaction: {scores['satisfaction']}%

Analyze these scores and provide helpful advice.
"""

    import json

    response = chat.invoke([
        SystemMessage(content=system_prompt),
        HumanMessage(content=user_prompt)
    ])

    data = json.loads(response.content)

    return data

