from langchain_google_genai import ChatGoogleGenerativeAI


class ResearchAgent:

    def __init__(self):

        self.llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash",
            temperature=0.3
        )

    def run(self, task):

        prompt = f"""
You are a research assistant.

TASK:
{task}

Provide concise research findings.
"""

        response = self.llm.invoke(prompt)

        return response.content