class FinancialDataAgent:
    def __init__(self, financial_data: dict):
        """
        financial_data: output from FinancialDataLoader
        """
        self.data = financial_data

    def _get_latest_two_periods(self, metric_dict: dict):
        periods = sorted(metric_dict.keys())
        if len(periods) < 2:
            return None, None, None, None

        prev_period = periods[-2]
        latest_period = periods[-1]

        return (
            prev_period,
            latest_period,
            metric_dict[prev_period],
            metric_dict[latest_period],
        )

    def _growth_rate(self, previous, current):
        if previous == 0 or previous is None:
            return None
        return round(((current - previous) / previous) * 100, 2)

    def compute_metrics(self) -> dict:
        results = {}

        # -------- Income Statement Metrics --------
        income_stmt = self.data.get("IncomeStatement", {})

        revenue = income_stmt.get("Revenue", {})
        net_income = income_stmt.get("NetIncome", {})

        rev_prev_p, rev_latest_p, rev_prev, rev_latest = self._get_latest_two_periods(
            revenue
        )
        ni_prev_p, ni_latest_p, ni_prev, ni_latest = self._get_latest_two_periods(
            net_income
        )

        if rev_latest and ni_latest:
            net_margin = round((ni_latest / rev_latest) * 100, 2)
        else:
            net_margin = None

        results["income_statement"] = {
            "revenue_yoy_growth_pct": self._growth_rate(rev_prev, rev_latest),
            "net_income_yoy_growth_pct": self._growth_rate(ni_prev, ni_latest),
            "net_profit_margin_pct": net_margin,
            "period_compared": f"{rev_prev_p} → {rev_latest_p}",
        }

        # -------- Cash Flow Metrics --------
        cashflow_stmt = self.data.get("CashFlowStatement", {})
        ocf = cashflow_stmt.get("OperatingCashFlow", {})

        ocf_prev_p, ocf_latest_p, ocf_prev, ocf_latest = self._get_latest_two_periods(
            ocf
        )

        results["cash_flow"] = {
            "operating_cash_flow_yoy_growth_pct": self._growth_rate(
                ocf_prev, ocf_latest
            ),
            "profit_vs_cash_flow_gap": (
                round(ni_latest - ocf_latest, 2)
                if ni_latest is not None and ocf_latest is not None
                else None
            ),
            "period_compared": f"{ocf_prev_p} → {ocf_latest_p}",
        }

        return results
