def build_financial_evidence(financial_data, metrics, validations):
    evidence = []

    # Raw financial data
    for stmt, accounts in financial_data.items():
        for account, periods in accounts.items():
            for period, value in periods.items():
                evidence.append(
                    f"{stmt} - {account} in {period} was {value}"
                )

    # Metrics
    for section, values in metrics.items():
        for key, val in values.items():
            evidence.append(
                f"{section} metric {key} is {val}"
            )

    # Validation flags
    for flag in validations.get("red_flags", []):
        evidence.append(f"Validation finding: {flag}")

    return evidence
