import argparse
import pandas as pd


def _get_bias_index(
    df: pd.Series,
    threshold: int,
) -> list[str]:
    """TODO: Docstring for _get_bias_indice_id_str.
    :returns: TODO

    """
    vc = df.value_counts()
    threshold_processed_vc = vc[vc < threshold]
    bias_index = threshold_processed_vc.index.tolist()

    return bias_index


def main(
    bias_percentage: int,
):
    """TODO: Docstring for main.

    :arg1: TODO
    :returns: TODO

    """
    input_df = pd.read_csv("/tmp/input.csv")

    if bias_percentage == 0:
        threshold = 0
    else:
        threshold = int(len(input_df) * (bias_percentage / 100))
    print("threshold=", threshold)

    conditions = input_df['indice_id_str'].isin(
        _get_bias_index(input_df['indice_id_str'], threshold)
    )
    print("bias_index=", _get_bias_index(input_df['indice_id_str'], threshold))
    input_df[conditions].to_csv("/tmp/output.csv", index=False)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--bias_percentage",
        type=int,
    )

    args = parser.parse_args()

    main(
        args.bias_percentage,
    )
