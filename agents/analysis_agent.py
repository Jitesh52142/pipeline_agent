from langchain_google_genai import ChatGoogleGenerativeAI


class AnalysisAgent:

    def __init__(self):

        self.llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash",
            temperature=0.3
        )

    def run(self, task):

        prompt = f"""
You are an analysis expert.

TASK:
{task}

Provide structured analysis.
"""

        response = self.llm.invoke(prompt)

        return response.content