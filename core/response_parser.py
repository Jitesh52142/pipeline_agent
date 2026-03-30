import json
import re
import logging

class ResponseParser:
    """
    Regex or JSON parsing logic to detect if the LLM wants to use a tool.
    Extracts: { tool: "web_search", input: "AI trends 2025" }
    """
    def parse_response(self, text):
        match = re.search(r"\{.*\}", text, re.DOTALL)
        if match:
            try:
                data = json.loads(match.group())
                if "tool" in data:
                    logging.info(f"Tool request detected: {data['tool']}")
                    return "tool", data
                else: 
                    logging.info("Final answer detected (JSON format)")
                    return "answer", text
            except json.JSONDecodeError:
                logging.info("Final answer detected (plain text)")
                return "answer", text
        else:
            logging.info("Final answer detected (plain text)")
            return "answer", text
