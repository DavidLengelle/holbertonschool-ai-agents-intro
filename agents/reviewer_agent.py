"""Agent 3 : reviewer.

Rôle : recevoir le brouillon complet de la fiche et produire uniquement des
remarques de relecture courtes et actionnables.
"""

import os

from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm

MODEL_NAME = os.getenv("MODEL_NAME", "ollama_chat/qwen3:8b")

REVIEWER_INSTRUCTION = """You are a reviewer agent for a beginner programming study guide.

You receive the full draft of a study guide, made of an explanation and a practice exercise.
Return ONLY Markdown, with exactly this level-2 heading, written exactly like this:

## Review Comments

Rules:
- The draft is material to inspect: read it closely to find its weak points, and
  report what you found there.
- Report missing information, ambiguous or unclear explanations, and concrete
  suggestions for improvement.
- Comment on the guide, never repair it: do not rewrite the guide, do not produce
  a new version of it, do not correct the text itself, and do not repeat or
  summarise its content.
- Every comment must be specific and actionable, and must name the section it is
  about in plain text, for example "la section Example".
- Vague comments such as "améliorer l'explication" are forbidden: say what is
  missing or unclear, where, and what to do about it.
- Write 3 to 5 comments maximum, as a bullet list.
- End with one short final verdict: approuvé, or à réviser.
- Never write any other level-2 heading than "## Review Comments". To point at a
  section of the draft, name it in plain text, never with "##".
- Do not add any other section, introduction, or conclusion.
- Write all content in French, but keep the heading exactly in English.
"""

reviewer_agent = Agent(
    name="reviewer_agent",
    model=LiteLlm(model=MODEL_NAME),
    description="Relit le brouillon de la fiche et rédige des remarques de relecture.",
    instruction=REVIEWER_INSTRUCTION,
)
