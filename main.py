"""Point d'entrée du générateur de fiches de révision."""

import asyncio
import re

from dotenv import load_dotenv
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types

from agents.explainer_agent import explainer_agent
from tools.file_writer import save_markdown_file
from tools.validation import validate_required_sections

load_dotenv()

APP_NAME = "study_guide"
USER_ID = "student"

THINK_BLOCK = re.compile(r"<think>.*?</think>", re.DOTALL)


def strip_thinking(text: str) -> str:
    """Retire les blocs de raisonnement éventuels du modèle."""
    return THINK_BLOCK.sub("", text).strip()


async def run_explainer(topic: str) -> str:
    """Fait tourner l'agent explainer sur un sujet et renvoie sa réponse."""
    session_service = InMemorySessionService()
    runner = Runner(
        agent=explainer_agent,
        app_name=APP_NAME,
        session_service=session_service,
    )
    session = await session_service.create_session(
        app_name=APP_NAME,
        user_id=USER_ID,
    )

    message = types.Content(role="user", parts=[types.Part(text=topic)])

    response = ""
    async for event in runner.run_async(
        user_id=USER_ID,
        session_id=session.id,
        new_message=message,
    ):
        if event.is_final_response() and event.content and event.content.parts:
            texte = "".join(
                part.text
                for part in event.content.parts
                if part.text and not getattr(part, "thought", False)
            )
            if texte:
                response = texte

    return strip_thinking(response)


async def main() -> None:
    topic = input("Topic: ")
    reponse = await run_explainer(topic)
    print(reponse)

    validation = validate_required_sections(reponse)
    if not validation["valid"]:
        print("Sections manquantes :")
        for section in validation["missing_sections"]:
            print(f"- {section}")

    print(save_markdown_file("output/study_guide.md", reponse))


if __name__ == "__main__":
    asyncio.run(main())