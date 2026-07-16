"""Agent 2 : practice designer.

Rôle : recevoir un sujet et son explication, puis produire un exercice
pratique court destiné à un débutant.
"""

import os

from dotenv import load_dotenv
from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm

load_dotenv()

MODEL_NAME = os.getenv("MODEL_NAME", "ollama_chat/qwen2.5:3b")

PRACTICE_DESIGNER_INSTRUCTION = """You are a practice designer agent for beginner programming students.

You receive one programming topic and an explanation of that topic.
Return ONLY Markdown, with exactly this level-2 heading, written exactly like this:

## Practice Exercise

Rules:
- The explanation is context only: read it to choose a relevant exercise, never
  repeat it, rephrase it, or summarise it.
- Design exactly one short, concrete exercise, doable in 10 to 20 minutes by a beginner.
- State the task first, then the expected input and the expected output when they
  are relevant to the exercise.
- End with one or two hints.
- Do not explain or teach the topic again.
- Do not give the solution, not even partially.
- Do not require a large application, a database, an external service, an API key,
  or any installation.
- Do not add any other section, introduction, or conclusion.
- Write all content in French, but keep the heading exactly in English.
"""

practice_designer_agent = Agent(
    name="practice_designer_agent",
    model=LiteLlm(model=MODEL_NAME),
    description="Conçoit un exercice pratique court à partir d'un sujet et de son explication.",
    instruction=PRACTICE_DESIGNER_INSTRUCTION,
)
