import streamlit as st
import os
import json
from dotenv import load_dotenv
load_dotenv()

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

st.set_page_config(page_title="Multi-Agent MD&A AI", layout="wide")

st.title("📊 Multi-Agent Financial Analyst (Automated MD&A AI)")

company = st.text_input("Enter Company Symbol", "AAPL")

if st.button("Generate MD&A"):
    with st.spinner("Analyzing financials..."):
        loader = FinancialDataLoader("data/raw/financials.csv")
        financial_data = loader.load_company_data(company)

        data_agent = FinancialDataAgent(financial_data)
        metrics = data_agent.compute_metrics()

        validation_agent = FinancialValidationAgent(metrics)
        validation = validation_agent.run_validations()

        trend_agent = TrendAnalysisAgent(api_key=os.getenv("OPENAI_API_KEY"))
        trends = trend_agent.analyze_trends(metrics, validation)

        risk_agent = RiskAnalysisAgent(api_key=os.getenv("OPENAI_API_KEY"))
        risks = risk_agent.analyze_risks(metrics, trends, validation)

        evidence_store = FinancialEvidenceStore()
        docs = build_financial_evidence(financial_data, metrics, validation)
        evidence_store.add_documents(docs)

        aggregator = InsightAggregator(
            metrics, trends, risks, validation, evidence_store
        )
        aggregated = aggregator.aggregate()

        writer = MDNAWriterAgent(api_key=os.getenv("OPENAI_API_KEY"))
        mdna = writer.generate_mdna(aggregated)

        explainability = ExplainabilityEngine(aggregated).build_explainability()

    st.subheader("📝 Generated MD&A")
    st.text(mdna)

    st.subheader("🔍 Explainability & Confidence")

    for section, info in explainability.items():
        st.markdown(f"### {section.replace('_', ' ').title()}")
        
        # Confidence score
        confidence_pct = int(info["confidence_score"] * 100)
        st.markdown(f"**Confidence:** {confidence_pct}%")
        st.progress(confidence_pct)
        
        # Evidence
        st.markdown("**Supporting Evidence:**")
        if info["supporting_evidence"]:
            for ev in info["supporting_evidence"]:
                st.markdown(f"- {ev}")
        else:
            st.markdown("_No supporting evidence available_")

