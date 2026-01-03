import pandas as pd
from collections import defaultdict


class FinancialDataLoader:
    def __init__(self, csv_path: str):
        self.csv_path = csv_path

    def load_company_data(self, company: str) -> dict:
        df = pd.read_csv(self.csv_path)

        # Filter company
        df = df[df["company"] == company]

        if df.empty:
            raise ValueError(f"No data found for company: {company}")

        structured_data = defaultdict(lambda: defaultdict(dict))

        for _, row in df.iterrows():
            statement = row["statement_type"]
            account = row["account_name"]
            period = str(row["period"])
            value = float(row["value"])

            structured_data[statement][account][period] = value

        return structured_data
