import argparse
import json
from pathlib import Path

import numpy as np
import pandas as pd

TARGET = "取引価格（総額）_log"

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("input_train_csv")
    parser.add_argument("input_test_csv")
    parser.add_argument("config_json")
    parser.add_argument("--verbose", "-v", action="store_true")
    args = parser.parse_args()

    train_df = pd.read_csv(args.input_train_csv)
    test_df = pd.read_csv(args.input_test_csv)

    test_df[TARGET] = np.nan  # shapeを合わせるため、目的変数のカラムを追加
    df = pd.concat([train_df, test_df])

    assert df.shape == (637351 + 19466, 28)

    # すべて欠損値のカラムとすべて同じ値のカラムは特徴量から除く
    remove_columns = []
    for column_name, distinct_value_count in df.nunique().iteritems():
        if distinct_value_count <= 1:
            remove_columns.append(column_name)
    if args.verbose:
        print(df.nunique())

    # TODO: 今後他のスクリプトでもconfigを更新すると思われる。コンテキストマネージャーとして書けるのでは？
    config_path = Path(args.config_json)
    config = {}
    if config_path.exists():
        with config_path.open() as fin:
            config = json.load(fin)
    config["remove_columns"] = remove_columns
    with config_path.open("w") as fout:
        json.dump(config, fout, ensure_ascii=False, indent=2)
