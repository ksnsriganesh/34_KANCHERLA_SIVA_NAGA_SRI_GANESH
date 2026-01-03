class FinancialValidationAgent:
    def __init__(self, metrics: dict):
        """
        metrics: output from FinancialDataAgent.compute_metrics()
        """
        self.metrics = metrics

    def run_validations(self) -> dict:
        flags = []

        income = self.metrics.get("income_statement", {})
        cash = self.metrics.get("cash_flow", {})

        rev_growth = income.get("revenue_yoy_growth_pct")
        ni_growth = income.get("net_income_yoy_growth_pct")
        net_margin = income.get("net_profit_margin_pct")
        ocf_growth = cash.get("operating_cash_flow_yoy_growth_pct")

        # Rule 1: Revenue growth but profit decline
        if rev_growth is not None and ni_growth is not None:
            if rev_growth > 0 and ni_growth < 0:
                flags.append(
                    "Revenue increased while net income declined, indicating margin pressure or rising costs."
                )

        # Rule 2: Low profit margin
        if net_margin is not None and net_margin < 10:
            flags.append(
                f"Net profit margin is low at {net_margin}%, which may impact long-term sustainability."
            )

        # Rule 3: Cash flow decline
        if ocf_growth is not None and ocf_growth < -10:
            flags.append(
                f"Operating cash flow declined sharply by {ocf_growth}%, raising liquidity concerns."
            )

        # Rule 4: Profit vs cash mismatch
        gap = cash.get("profit_vs_cash_flow_gap")
        if gap is not None and gap < 0:
            flags.append(
                "Reported profits are not fully supported by operating cash flows, indicating potential earnings quality risk."
            )

        return {
            "red_flags": flags,
            "flag_count": len(flags),
        }
