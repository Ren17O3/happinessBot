from fastapi import FastAPI
from backend.models import Questionnaire, ChatMessage
from backend.scoring import calculate_scores
from backend.llm import generate_relationship_advice, chat
from langchain_core.messages import HumanMessage, SystemMessage


app = FastAPI()


# ------------------------------------------------
# Home Route
# ------------------------------------------------

@app.get("/")
def home():
    return {"message": "Couple Compatibility API running"}


# ------------------------------------------------
# Questionnaire Analysis Endpoint
# ------------------------------------------------

@app.post("/submit")
def submit_answers(data: Questionnaire):

    answers = data.answers

    # Calculate compatibility scores
    scores = calculate_scores(answers)

    # Generate AI insights (strength, focus area, suggestion)
    advice = generate_relationship_advice(scores)

    return {
        "scores": scores,
        "insights": advice
    }


# ------------------------------------------------
# Chat Endpoint
# ------------------------------------------------

@app.post("/chat")
def chat_with_user(data: ChatMessage):

    scores = data.scores

    # Context given to chatbot
    context = f"""
Relationship Scores:
Emotional Connection: {scores['emotional']}%
Communication: {scores['communication']}%
Trust: {scores['trust']}%
Conflict Resolution: {scores['conflict']}%
Relationship Satisfaction: {scores['satisfaction']}%
"""

    # Chat system prompt (different from analysis prompt)
    chat_prompt = """
You are an emotionally intelligent relationship assistant.

The user already completed a compatibility questionnaire.
You have access to their relationship scores.

Your job:
- Answer the user's question conversationally
- Give thoughtful relationship guidance
- Be supportive but realistic
- Avoid structured lists like "Strength / Focus Area / Suggestion"
- Respond like a natural conversation

Keep responses concise and helpful.
"""

    response = chat.invoke([
        SystemMessage(content=chat_prompt),
        HumanMessage(content=context + "\nUser Question: " + data.message)
    ])

    return {"reply": response.content}