import logging

class PromptBuilder:
    """
    Optimized PromptBuilder for minimal token usage.
    """
    def __init__(self, system_prompt="You are a helpful AI assistant."):
        self.system_prompt = system_prompt
        self.roles = {
            "research_agent": "Researcher (gather data).",
            "analysis_agent": "Analyst (derive insights).",
            "writer_agent": "Writer (create report)."
        }

    def build_prompt(self, agent_id, task, context=""):
        role = self.roles.get(agent_id, "Assistant.")
        
        # Concise prompt structure
        prompt = f"""
SYSTEM: {self.system_prompt}
ROLE: {role}
TASK: {task}
CONTEXT: {context if context else "None"}

Short instructions:
1. Use CONTEXT.
2. Tool use (JSON): {{ "tool": "name", "input": "..." }}
3. Tools: 'web_search', 'data_analysis'.
4. Final answer: plain text.
"""
        return prompt.strip()
