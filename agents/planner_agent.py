import json
import logging
import re
from core.llm_interface import LLMInterface
from core.response_parser import ResponseParser

class PlannerAgent:
    """
    Concise Planner Agent to minimize credits.
    """
    def __init__(self):
        self.llm = LLMInterface()
        self.parser = ResponseParser()

    def plan(self, user_request):
        logging.info(f"PlannerAgent: Planning for '{user_request}'")

        # Compact planning prompt
        prompt = f"""
SYSTEM: Planner Agent.
TASK: Break request into sequence tasks for agents.
AGENTS: 
- research_agent (web_search)
- analysis_agent (trends)
- writer_agent (report)

RULES: Max 5 tasks. Return ONLY valid JSON.
Format:
{{ "tasks": [ {{ "task": "...", "agent": "name" }} ] }}

USER REQUEST:
{user_request}
"""
        response = self.llm.generate(prompt)

        try:
            json_match = re.search(r"\{.*\}", response, re.DOTALL)
            if json_match:
                tasks_data = json.loads(json_match.group())
                return tasks_data.get("tasks", [])
        except Exception as e:
            logging.error(f"PlannerAgent: Parsing error: {e}")
            return []
        
        return []