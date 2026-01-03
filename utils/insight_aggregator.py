class InsightAggregator:
    def __init__(
        self,
        metrics: dict,
        trends: dict,
        risks: dict,
        validation: dict,
        evidence_store
    ):
        self.metrics = metrics
        self.trends = trends
        self.risks = risks
        self.validation = validation
        self.evidence_store = evidence_store

    def aggregate(self) -> dict:
        aggregated = {
            "financial_performance": self.metrics,
            "trend_analysis": self.trends,
            "risk_analysis": self.risks,
            "validation_flags": self.validation.get("red_flags", []),
            "supporting_evidence": {}
        }

        # Attach evidence for each trend
        for key, insight in self.trends.items():
            aggregated["supporting_evidence"][key] = (
                self.evidence_store.retrieve(insight)
                if insight else []
            )

        # Attach evidence for each risk
        for key, risk in self.risks.items():
            aggregated["supporting_evidence"][key] = (
                self.evidence_store.retrieve(risk)
                if risk else []
            )

        return aggregated
