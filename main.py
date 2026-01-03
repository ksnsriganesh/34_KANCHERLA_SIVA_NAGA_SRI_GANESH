from utils.loader import FinancialDataLoader
from agents.data_agent import FinancialDataAgent
from utils.validators import FinancialValidationAgent
from agents.trend_agent import TrendAnalysisAgent
from agents.risk_agent import RiskAnalysisAgent
from rag.vector_store import FinancialEvidenceStore
from rag.build_evidence import build_financial_evidence
from utils.insight_aggregator import InsightAggregator
from agents.writer_agent import MDNAWriterAgent
from utils.explainability import ExplainabilityEngine


import json
import os
from dotenv import load_dotenv
load_dotenv()


if __name__ == "__main__":
    # print(os.getenv("OPENAI_API_KEY"))
    loader = FinancialDataLoader("data/raw/financials.csv")
    financial_data = loader.load_company_data("AAPL")

    data_agent = FinancialDataAgent(financial_data)
    metrics = data_agent.compute_metrics()

    validation_agent = FinancialValidationAgent(metrics)
    validation_results = validation_agent.run_validations()

    trend_agent = TrendAnalysisAgent(api_key=os.getenv("OPENAI_API_KEY"))
    trends = trend_agent.analyze_trends(metrics, validation_results)

    print("TRENDS:")
    # print(json.dumps(trends, indent=4))

    risk_agent = RiskAnalysisAgent(api_key=os.getenv("OPENAI_API_KEY"))
    risks = risk_agent.analyze_risks(metrics, trends, validation_results)

    print("RISKS:")
    #print(json.dumps(risks, indent=4))
    #

    evidence_store = FinancialEvidenceStore()

    documents = build_financial_evidence(
        financial_data,
        metrics,
        validation_results
    )

    evidence_store.add_documents(documents)

    query = "Why did profitability decline?"
    supporting_evidence = evidence_store.retrieve(query)

    #print("\nEVIDENCE:")
    # for e in supporting_evidence:
    #     print("-", e)

    aggregator = InsightAggregator(
    metrics=metrics,
    trends=trends,
    risks=risks,
    validation=validation_results,
    evidence_store=evidence_store
    )

    aggregated_insights = aggregator.aggregate()

    # print("\nAGGREGATED INSIGHTS:")
    import json
    print(json.dumps(aggregated_insights, indent=2))

    writer_agent = MDNAWriterAgent(api_key=os.getenv("OPENAI_API_KEY"))
    mdna_report = writer_agent.generate_mdna(aggregated_insights)

   

    # print("\nGENERATED MD&A REPORT:\n")
    # print(mdna_report)

    explainability_engine = ExplainabilityEngine(aggregated_insights)
    explainability_report = explainability_engine.build_explainability()

    print("\nEXPLAINABILITY & CONFIDENCE:\n")
    print(json.dumps(explainability_report, indent=2))