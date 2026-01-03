from openai import OpenAI
import json


class MDNAWriterAgent:
    def __init__(self, api_key: str):
        self.client = OpenAI(api_key=api_key)

    def generate_mdna(self, aggregated_insights: dict) -> str:
        prompt = f"""
You are a professional financial analyst writing the Management Discussion & Analysis (MD&A) section of a financial report.

You must ONLY use the provided insights.
Do NOT invent facts.
Do NOT introduce new numbers or assumptions.

STRUCTURED INSIGHTS:
{json.dumps(aggregated_insights, indent=2)}

Write a clear and professional MD&A with the following sections:
1. Overview
2. Financial Performance
3. Cash Flow Analysis
4. Key Risks and Outlook

Guidelines:
- Use formal MD&A tone
- Explain trends and risks clearly
- Keep it concise but complete
"""

        response = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You write accurate and conservative financial MD&A reports."},
                {"role": "user", "content": prompt},
            ],
            temperature=0.2,
        )

        return response.choices[0].message.content
