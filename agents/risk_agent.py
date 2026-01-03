from openai import OpenAI
import json


class RiskAnalysisAgent:
    def __init__(self, api_key: str):
        self.client = OpenAI(api_key=api_key)

    def analyze_risks(
        self,
        metrics: dict,
        trends: dict,
        validation: dict
    ) -> dict:
        prompt = f"""
You are a senior financial risk analyst.

Your task is to identify key financial risks based ONLY on the information provided.
Do NOT invent data.
Do NOT repeat trends unless needed to explain risk.

METRICS:
{json.dumps(metrics, indent=2)}

TRENDS:
{json.dumps(trends, indent=2)}

RED FLAGS:
{json.dumps(validation, indent=2)}

Instructions:
- Identify material financial risks
- Explain why each risk matters
- Use professional MD&A risk language
- Output JSON with keys:
  - liquidity_risk
  - profitability_risk
  - earnings_quality_risk
"""

        response = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a conservative financial risk analyst."},
                {"role": "user", "content": prompt},
            ],
            temperature=0.2,
            response_format={"type": "json_object"},
        )

        content = response.choices[0].message.content
        return json.loads(content)
