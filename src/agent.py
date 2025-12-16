# ============ Importação ============= #
import os
import sys

from dotenv import load_dotenv, find_dotenv

from agno.agent import Agent
from agno.models.groq import Groq
from agno.db.sqlite import SqliteDb
from agno.tools.tavily import TavilyTools
from agno.os import AgentOS

from transcription_reader import get_creator_transcriptions, list_available_creators


# ============ Constantes ============= #
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

_ = load_dotenv(find_dotenv(".env"))
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")
DB = SqliteDb(
    db_file="temp/storage.db",
    session_table="agent_sessions"
)

# ============== Código =============== #
copywrite = Agent(
    model=Groq(api_key=GROQ_API_KEY, id="openai/gpt-oss-120b"),  # llama-3.3-70b-versatile
    id="copywrite-agent",
    name="copywrite",
    description="",
    instructions=open("prompts/copywriter.md", "r", encoding="utf-8").read(),
    db=DB,
    add_history_to_context=True,
    num_history_runs=3,
    enable_user_memories=True,
    add_memories_to_context=True,

    tools=[
        TavilyTools(api_key=TAVILY_API_KEY),
        get_creator_transcriptions,
        list_available_creators,
    ],
)

agent_os = AgentOS(
    id="copywrite-os",
    name="Copywriting AgentOS",
    description="AgentOS para copywriting",
    agents=[copywrite],
)
app = agent_os.get_app()


# ============= Execução ============== #
if __name__ == "__main__":
    agent_os.serve(app="src.agent:app", host="localhost", port=7777, reload=True)
