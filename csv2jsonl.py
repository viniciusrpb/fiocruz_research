import pandas as pd

csvpath = "faq.csv"

jsonlpath = "faq.jsonl"

df = pd.read_csv(csv_path)
df.to_json(jsonl_path, orient="records", lines=True, force_ascii=False)
