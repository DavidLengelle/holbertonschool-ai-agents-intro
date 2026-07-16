"""Point d'entrée du générateur de fiches de révision."""

import asyncio
import os
import re

from dotenv import load_dotenv
from google.adk.agents import Agent
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types
from litellm.exceptions import APIConnectionError

from agents.explainer_agent import explainer_agent
from agents.practice_designer_agent import practice_designer_agent
from agents.reviewer_agent import reviewer_agent
from tools.file_writer import save_markdown_file
from tools.validation import validate_required_sections

load_dotenv()

APP_NAME = "study_guide"
USER_ID = "student"
OUTPUT_PATH = "output/study_guide.md"
REQUIRED_ENV_VARS = ["OLLAMA_API_BASE", "MODEL_NAME"]

THINK_BLOCK = re.compile(r"<think>.*?</think>", re.DOTALL)


def strip_thinking(text: str) -> str:
    """Retire les blocs de raisonnement éventuels du modèle."""
    return THINK_BLOCK.sub("", text).strip()


def announce(etape: str) -> None:
    """Affiche une étape en cours, distincte du contenu de la fiche."""
    print(f"\n=== {etape} (plusieurs minutes) ===\n", flush=True)


def ollama_tag(model_name: str) -> str:
    """Renvoie le tag Ollama d'un modèle, sans le préfixe du fournisseur LiteLLM."""
    if "/" in model_name:
        return model_name.split("/", 1)[1]
    return model_name


def find_missing_env_vars() -> list:
    """Renvoie les variables d'environnement requises qui ne sont pas définies."""
    manquantes = []
    for variable in REQUIRED_ENV_VARS:
        if not os.getenv(variable):
            manquantes.append(variable)
    return manquantes


async def run_agent(agent: Agent, entree: str) -> str:
    """Fait tourner un agent sur un texte d'entrée et renvoie sa réponse finale."""
    session_service = InMemorySessionService()
    runner = Runner(
        agent=agent,
        app_name=APP_NAME,
        session_service=session_service,
    )
    session = await session_service.create_session(
        app_name=APP_NAME,
        user_id=USER_ID,
    )

    message = types.Content(role="user", parts=[types.Part(text=entree)])

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


async def run_explainer(topic: str) -> str:
    """Fait tourner l'agent explainer sur un sujet et renvoie son explication."""
    return await run_agent(explainer_agent, topic)


async def run_practice_designer(topic: str, explanation: str) -> str:
    """Fait tourner l'agent practice designer et renvoie son exercice."""
    return await run_agent(
        practice_designer_agent,
        f"Topic: {topic}\n\nExplanation:\n{explanation}",
    )


async def run_reviewer(draft: str) -> str:
    """Fait tourner l'agent reviewer sur le brouillon et renvoie ses sections."""
    return await run_agent(reviewer_agent, f"Draft:\n{draft}")


def assemble_draft(explanation: str, exercise: str) -> str:
    """Assemble le brouillon de la fiche soumis au reviewer."""
    return f"{explanation}\n\n{exercise}"


def assemble_final(draft: str, review: str) -> str:
    """Assemble la fiche finale à partir du brouillon et des sections du reviewer."""
    return f"{draft}\n\n{review}"


def report_validation(fiche: str) -> None:
    """Affiche les sections requises absentes de la fiche, sans rien bloquer."""
    validation = validate_required_sections(fiche)
    if validation["valid"]:
        print("Validation : les 8 sections requises sont présentes.")
        return

    print("Validation : sections requises manquantes :")
    for section in validation["missing_sections"]:
        print(f"- {section}")
    print("La fiche est enregistrée quand même : relancer pour une autre sortie.")


async def build_study_guide(topic: str) -> str:
    """Fait tourner les trois agents sur un sujet et renvoie la fiche assemblée."""
    announce("Agent 1/3 : explainer, rédaction de l'explication")
    explication = await run_explainer(topic)
    print(explication)

    announce("Agent 2/3 : practice designer, conception de l'exercice")
    exercice = await run_practice_designer(topic, explication)
    print(exercice)

    brouillon = assemble_draft(explication, exercice)

    announce("Agent 3/3 : reviewer, relecture et sections finales")
    revue = await run_reviewer(brouillon)
    print(revue)

    return assemble_final(brouillon, revue)


async def main() -> None:
    """Vérifie la configuration et le sujet, produit la fiche puis l'enregistre."""
    manquantes = find_missing_env_vars()
    if manquantes:
        print("Configuration incomplète, variables d'environnement manquantes :")
        for variable in manquantes:
            print(f"- {variable}")
        print("Les définir dans le fichier .env à la racine du projet, "
              "sur le modèle de .env.example.")
        return

    topic = input("Topic: ").strip()
    if not topic:
        print("Sujet vide : indiquer un sujet, par exemple "
              "« les boucles for en Python ».")
        return

    try:
        fiche = await build_study_guide(topic)
    except APIConnectionError as erreur:
        modele = os.getenv("MODEL_NAME", "")
        print(f"\nLe modèle local n'a pas répondu : {erreur}")
        print(f"Vérifier que le service Ollama tourne et répond (ollama list), "
              f"et que le modèle {modele} de MODEL_NAME est bien téléchargé "
              f"(ollama pull {ollama_tag(modele)}).")
        return

    print()
    report_validation(fiche)
    print(save_markdown_file(OUTPUT_PATH, fiche))


if __name__ == "__main__":
    asyncio.run(main())
