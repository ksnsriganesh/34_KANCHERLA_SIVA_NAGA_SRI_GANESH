class ExplainabilityEngine:
    def __init__(self, aggregated_insights: dict):
        self.insights = aggregated_insights

    def build_explainability(self) -> dict:
        explanation = {}
        evidence_map = self.insights.get("supporting_evidence", {})
        flags_map = self.insights.get("validation_flags", {})


        for section, evidence in evidence_map.items():
            section_flags = flags_map.get(section, [])
            confidence = self._compute_confidence(evidence, section_flags)


            explanation[section] = {
                "supporting_evidence": evidence,
                "confidence_score": confidence
            }

        return explanation

    def _compute_confidence(self, evidence: list, flags: list) -> float:
        if not evidence:
            return 0.3  # low confidence if no evidence

        base_score = min(1.0, 0.5 + 0.1 * len(evidence))
        penalty = 0.05 * len(flags)

        return round(max(0.0, base_score - penalty), 2)
