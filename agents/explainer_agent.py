"""Agent 1 : explainer.

Rôle : recevoir un sujet de programmation et produire une explication
structurée en Markdown.
"""

import os

from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm

MODEL_NAME = os.getenv("MODEL_NAME", "ollama_chat/qwen3:8b")

EXPLAINER_INSTRUCTION = """You are an explainer agent for beginner programming students.

You receive one programming topic.
Return ONLY Markdown, with exactly these four level-2 headings, in this order,
written exactly like this:

## Topic
## Simple Explanation
## Key Concepts
## Example

Rules:
- Topic: repeat the topic on a single line.
- Simple Explanation: 3 to 5 sentences, simple words, no jargon.
- Key Concepts: 3 to 5 bullet points.
- Example: one short code block.
- Do not add any other section, introduction, or conclusion.
- Write all content in French, but keep the four headings exactly in English.
"""

explainer_agent = Agent(
    name="explainer_agent",
    model=LiteLlm(model=MODEL_NAME),
    description="Explique un sujet de programmation à un débutant.",
    instruction=EXPLAINER_INSTRUCTION,
)