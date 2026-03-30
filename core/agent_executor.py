import logging
import json
from .prompt_builder import PromptBuilder
from .llm_interface import LLMInterface
from .response_parser import ResponseParser
from .tool_executor import ToolExecutor

class AgentExecutor:
    """
    The runtime loop for a specific agent. 
    It manages the Thought-Action-Observation cycle.
    """
    def __init__(self, context_manager):
        self.context_manager = context_manager
        self.prompt_builder = PromptBuilder()
        self.llm = LLMInterface()
        self.parser = ResponseParser()
        self.tool_executor = ToolExecutor()

    def execute(self, task):
        """
        Agent runtime loop.
        Loop: Build Prompt → LLM Call → Tool Needed? → Yes/No branches
        """
        agent_id = task.get("agent", "research_agent")
        task_description = task.get("task", "")
        
        logging.info(f"AgentExecutor: Starting execution loop for {agent_id} on task: {task_description}")

        # Cumulative context for THIS agent session
        agent_context = self.context_manager.get_context()
        
        # We can limit number of iterations to prevent infinite loops
        max_iterations = 3
        for i in range(max_iterations):
            # 1. Build prompt
            prompt = self.prompt_builder.build_prompt(agent_id, task_description, agent_context)

            # 2. Call LLM
            response = self.llm.generate(prompt)

            # 3. Check for tool usage
            response_type, result = self.parser.parse_response(response)

            if response_type == "tool":
                tool_name = result["tool"]
                tool_input = result["input"]

                logging.info(f"AgentExecutor: Iteration {i+1} calling tool {tool_name}")

                # 4. Execute tool
                observation = self.tool_executor.execute_tool(tool_name, tool_input)

                # 5. Result update
                # Add tool result to the local agent context for the next iteration
                agent_context += f"\n- Tool: {tool_name}\n- Result: {observation}\n"
                
                logging.info(f"AgentExecutor: Iteration {i+1} tool call complete.")
            else:
                # 6. Task complete
                logging.info(f"AgentExecutor: Task finalized at iteration {i+1}.")
                return response

        logging.warning("AgentExecutor: Max iterations reached, returning last response.")
        return response