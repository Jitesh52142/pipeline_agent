from langchain_google_genai import ChatGoogleGenerativeAI


class WriterAgent:

    def __init__(self):

        self.llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash",
            temperature=0.3
        )

    def run(self, task):

        prompt = f"""
You are a professional report writer.

TASK:
{task}

Write a clear and concise report.
"""

        response = self.llm.invoke(prompt)

        return response.content