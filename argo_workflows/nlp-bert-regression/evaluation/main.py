import typing as t
import argparse

import numpy as np
import pandas as pd
import mlflow


def pearson_corr(
    x: np.ndarray,
    y: np.ndarray,
) -> float:
    """
    This function returns the pearson correlation coefficient of peared
     one-dimension vectors.
    """
    return np.corrcoef(x, y).reshape(-1)[1]


def main(
    test_data_file_path: str,
    label_field_name: str,
    predicted_label_field_name: str,
):
    """TODO: Docstring for main.

    :returns: TODO

    """
    test_df = pd.read_csv(test_data_file_path)
    label = test_df[label_field_name].values
    predicted_label = test_df[predicted_label_field_name].values
    print(label)
    print(predicted_label)
    print(pearson_corr(label, predicted_label))

    return


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--test_data_file_path",
        type=str,
        default="/tmp/predict.csv"
    )
    parser.add_argument(
        "--label_field_name",
        type=str,
        default="label"
    )
    parser.add_argument(
        "--predicted_label_field_name",
        type=str,
        default="predicted_label"
    )
    args = parser.parse_args()

    main(
        args.test_data_file_path,
        args.label_field_name,
        args.predicted_label_field_name,
    )
