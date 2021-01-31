import argparse
from glob import glob

import pandas as pd

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("train_data_dir")
    parser.add_argument("concatenated_csv")
    args = parser.parse_args()

    paths = glob(f'{args.train_data_dir.rstrip("/")}/*')
    train_dfs = []
    for path in paths:
        train_df = pd.read_csv(path)
        train_dfs.append(train_df)

    train_df = pd.concat(train_dfs)
    train_df.reset_index(drop=True, inplace=True)

    assert train_df.shape == (637351, 28)

    train_df.to_csv(args.concatenated_csv, index=False)
