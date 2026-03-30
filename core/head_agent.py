import logging


class HeadAgent:
    """
    Head Agent (Router)

    Responsible for deciding which worker agent should execute
    a given task in the multi-agent pipeline.
    """

    VALID_AGENTS = [
        "research_agent",
        "analysis_agent",
        "writer_agent"
    ]

    def __init__(self, llm):
        """
        llm : LLM instance (Gemini / OpenAI / LangChain model)
        """
        self.llm = llm

    def build_prompt(self, task: str) -> str:
        """
        Builds the routing prompt for the LLM.
        """

        return f"""
You are the Head Agent (Task Router) in a multi-agent system.

Your job is to decide which agent should execute a given task.

Available agents:

1. research_agent
   Use for:
   - research
   - finding information
   - searching the web
   - collecting data

2. analysis_agent
   Use for:
   - reasoning
   - system design
   - architecture
   - data analysis
   - technical planning

3. writer_agent
   Use for:
   - writing reports
   - documentation
   - summarization
   - formatting final output


Rules:
- Choose ONLY ONE agent
- Do NOT invent new agent names
- Return ONLY the agent name
- Do NOT explain your answer

Valid outputs:

research_agent
analysis_agent
writer_agent


TASK:
{task}

Return the correct agent.
"""

    def route_task(self, task: str) -> str:
        """
        Determines which agent should handle the task.
        """

        try:

            prompt = self.build_prompt(task)

            # call LLM
            response = self.llm.invoke(prompt)

            agent_name = response.strip().lower()

            # validation
            if agent_name not in self.VALID_AGENTS:
                logging.warning(
                    f"HeadAgent returned invalid agent '{agent_name}'. Defaulting to analysis_agent."
                )
                agent_name = "analysis_agent"

            logging.info(f"HeadAgent routed task '{task}' → {agent_name}")

            return agent_name

        except Exception as e:

            logging.error(f"HeadAgent routing failed: {e}")

            # safe fallback
            return "analysis_agent"