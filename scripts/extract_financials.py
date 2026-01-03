import json
import pandas as pd
from io import StringIO


def load_company_financials(
   
    company_name: str
) -> pd.DataFrame:
    """
    Load and normalize SEC financial data for a given company name.

    Returns a DataFrame with columns:
    - statement_type
    - account_name
    - period
    - value
    """
    json_path="./2017q2.json"
    # -------------------------
    # Load JSON
    # -------------------------
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    # -------------------------
    # Load SEC tables
    # -------------------------
    num_df = pd.read_csv(StringIO(data["num.txt"]), sep="\t")
    sub_df = pd.read_csv(StringIO(data["sub.txt"]), sep="\t")
    tag_df = pd.read_csv(StringIO(data["tag.txt"]), sep="\t")
    pre_df = pd.read_csv(StringIO(data["pre.txt"]), sep="\t")

    # -------------------------
    # Find company in sub.txt
    # -------------------------
    company_rows = sub_df[
        sub_df["name"].str.contains(company_name, case=False, na=False)
    ]

    if company_rows.empty:
        raise ValueError(f"No SEC filings found for company: {company_name}")

    # -------------------------
    # Get filing IDs (adsh)
    # -------------------------
    company_adsh = company_rows["adsh"].unique()

    # -------------------------
    # Filter numeric data
    # -------------------------
    company_num = num_df[num_df["adsh"].isin(company_adsh)]

    # -------------------------
    # Build lookup tables
    # -------------------------
    tag_lookup = (
        tag_df[["tag", "tlabel"]]
        .drop_duplicates()
        .set_index("tag")["tlabel"]
        .to_dict()
    )

    pre_lookup = (
        pre_df[["tag", "stmt"]]
        .drop_duplicates()
        .set_index("tag")["stmt"]
        .to_dict()
    )

    stmt_map = {
        "IS": "Income Statement",
        "BS": "Balance Sheet",
        "CF": "Cash Flow Statement"
    }

    period_lookup = (
        company_rows[["adsh", "fy", "fp"]]
        .drop_duplicates()
        .set_index("adsh")
        .apply(lambda r: f"{int(r['fy'])}{r['fp']}", axis=1)
        .to_dict()
    )

    # -------------------------
    # Normalize rows
    # -------------------------
    normalized_rows = []

    for _, row in company_num.iterrows():
        tag = row["tag"]

        if tag not in tag_lookup or tag not in pre_lookup:
            continue

        normalized_rows.append({
            "statement_type": stmt_map.get(pre_lookup[tag], pre_lookup[tag]),
            "account_name": tag_lookup[tag],
            "period": period_lookup.get(row["adsh"], "UNKNOWN"),
            "value": float(row["value"])
        })

    return pd.DataFrame(normalized_rows)