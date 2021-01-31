import argparse
import csv
import json
from collections import Counter
from pathlib import Path

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("data_csv")
    parser.add_argument("config_json")
    parser.add_argument("output_root_dir")
    args = parser.parse_args()

    config_path = Path(args.config_json)
    config = {}
    if config_path.exists():
        with config_path.open() as fin:
            config = json.load(fin)
    remove_columns = config.get("remove_columns", [])
    remove_columns_set = set(remove_columns)

    output_root_path = Path(args.output_root_dir)
    output_root_path.mkdir(parents=True, exist_ok=True)

    with open(args.data_csv) as fin:
        reader = csv.DictReader(fin)
        rows = list(reader)

    columns = rows[0].keys()
    for column in columns:
        if column in remove_columns_set:
            continue
        # csvなのでrow[column]は文字列。欠損の場合は空文字''になる
        # csvの中にNaNという文字列は登場しないと仮定して、欠損していることが分かるように置き換える
        values = [row[column] if row[column] else "NaN" for row in rows]
        counter = Counter(values)
        with open(output_root_path / f"{column}.csv", "w") as fout:
            writer = csv.writer(fout)
            writer.writerows(counter.most_common())
