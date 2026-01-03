from openai import OpenAI
import json


class TrendAnalysisAgent:
    def __init__(self, api_key: str):
        self.client = OpenAI(api_key=api_key)

    def analyze_trends(self, metrics: dict, validation: dict) -> dict:
        prompt = f"""
You are a financial analyst.

Your task is to interpret company financial performance trends based ONLY on the provided metrics and validation flags.
Do NOT invent numbers.
Do NOT add assumptions.

METRICS:
{json.dumps(metrics, indent=2)}

RED FLAGS:
{json.dumps(validation, indent=2)}

Instructions:
- Identify revenue, profitability, and cash flow trends
- Explain performance in professional MD&A-style language
- Be concise and factual
- Output in JSON format with keys:
  - revenue_trend
  - profitability_trend
  - cash_flow_trend
"""

        response = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a cautious financial analyst."},
                {"role": "user", "content": prompt},
            ],
            temperature=0.2,
            response_format={"type": "json_object"},
        )


        content = response.choices[0].message.content

        return json.loads(content)
