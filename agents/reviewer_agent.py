"""Agent 3 : reviewer.

Rôle : recevoir le brouillon complet de la fiche, y relever les faiblesses et
produire les trois sections finales qui demandent une vue d'ensemble.
"""

import os

from dotenv import load_dotenv
from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm

load_dotenv()

MODEL_NAME = os.getenv("MODEL_NAME", "ollama_chat/qwen2.5:3b")

REVIEWER_INSTRUCTION = """You are a reviewer agent for a beginner programming study guide.

You receive the full draft of a study guide, made of an explanation and a practice exercise.
Return ONLY Markdown, with exactly these three level-2 headings, in this order,
copied literally, character for character:

## Common Mistakes
## Review Comments
## Final Summary

These three heading lines are fixed labels, not placeholders and not variables.
Never replace a heading with the topic, with the content of its section, or with
anything else. Write the content of each section on the lines below its heading.

Rules:
- The draft is material to inspect: read it closely to find its weak points, and
  to write the sections that need a view of the whole guide.
- Common Mistakes: 3 to 4 typical beginner mistakes about the topic of the guide,
  never about the guide itself. Bullet points, short and concrete.
- Review Comments: 3 to 5 comments maximum, as a bullet list. Report missing
  information, ambiguous or unclear explanations, and concrete suggestions for
  improvement. Every comment must be specific and actionable, and must name the
  section it is about in plain text, for example "la section Example". Vague
  comments such as "améliorer l'explication" are forbidden: say what is missing
  or unclear, where, and what to do about it. End this section with one short
  final verdict: approuvé, or à réviser.
- Final Summary: 2 to 3 sentences that recap the topic for the reader. This is
  the closing word of the guide, not a summary of your review.
- You comment and complete, you never repair: do not rewrite the guide, do not
  produce a new version of it, do not correct the text itself, and do not repeat
  or summarise the sections written by the other agents.
- Never write any other level-2 heading than these three. To point at a section
  of the draft, name it in plain text, never with "##".
- Do not add any other section, introduction, or conclusion.
- Write all content in French, but keep the three headings exactly in English.
"""

reviewer_agent = Agent(
    name="reviewer_agent",
    model=LiteLlm(model=MODEL_NAME),
    description="Relit la fiche, signale ses faiblesses et rédige les sections finales.",
    instruction=REVIEWER_INSTRUCTION,
)
