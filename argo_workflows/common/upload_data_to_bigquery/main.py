import os
import argparse
from typing import List

import pandas as pd
from google.cloud import bigquery


def main(
    project_id: str,
    db_name: str,
    table_name: str,
    dtype_dict: dict,
    id_field_names: List[str],
    update_field_names: List[str],
):
    """Upsert csv data into specified BigQuery database.

    BigQuery (standard SQL) don't support UPSERT (UPDATA/INSERT), so this
    function create temporary table named "temp_[existing_table_name]" and
    merge the table into target table.

    :param project_id: Name of GCP project that has database
    :type project_id: str
    :param db_name: Name of BigQuery database
    :type db_name: str
    :param table_name: Table name of BigQuery database
    :type table_name: str
    :param dtype_dict: Data type dict of input csv file
    :type dtype_dict: dict
    :param id_field_names: Id field names of input csv file
        (Used as composite key)
    :type id_field_names: list
    :param update_field_names: The field names you want to update
    :type update_field_names: list

    """
    client = bigquery.Client()
    query = f"""
    CREATE TABLE IF NOT EXISTS
        `{project_id}.{db_name}.temp_{table_name}`
    LIKE
        `{project_id}.{db_name}.{table_name}`;
    """

    query_job = client.query(query)
    _ = (
        query_job
        .result()
    )

    df = pd.read_csv('/tmp/input.csv')
    df = df.astype(dtype_dict)
    print(df.head())
    print(df.dtypes)
    query_job = client.load_table_from_dataframe(
        df,
        ".".join([project_id, db_name, "temp_" + table_name])
    )
    _ = (
        query_job
        .result()
    )

    columns = set(df.columns) & set(update_field_names)
    update_set_condition = ", ".join([
        f"target.{column} = tmp.{column}"
        for column in columns
    ])
    update_on_condition = " AND ".join([
        f"target.{id_field_name} = tmp.{id_field_name}"
        for id_field_name in id_field_names
    ])
    query = f"""
    MERGE
        `{project_id}.{db_name}.{table_name}` target
    USING
        `{project_id}.{db_name}.temp_{table_name}` tmp
    ON
        {update_on_condition}
    WHEN MATCHED THEN
        UPDATE SET {update_set_condition}
    WHEN NOT MATCHED THEN
        INSERT ROW
    """

    query_job = client.query(query)
    _ = (
        query_job
        .result()
        .to_dataframe()
    )

    query = f"""
    DROP TABLE
        `{project_id}.{db_name}.temp_{table_name}`
    """

    query_job = client.query(query)
    _ = (
        query_job
        .result()
        .to_dataframe()
    )

    return


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--project_id',
        help='BigQuery table name (endpoint)',
        default=os.getenv(
            'PROJECT_ID',
            None,
        ),
    )
    parser.add_argument(
        '--db_name',
        help='BigQuery table name (endpoint)',
        default=os.getenv(
            'DB_NAME',
            None,
        ),
    )
    parser.add_argument(
        '--table_name',
        help='BigQuery table name (endpoint)',
        default=os.getenv(
            'TABLE_NAME',
            None,
        ),
    )
    parser.add_argument(
        '--dtype_dict',
        help='BigQuery table name (endpoint)',
        default=os.getenv(
            'DTYPE_DICT',
            None,
        ),
    )
    parser.add_argument(
        '--id_field_names',
        help='BigQuery table name (endpoint)',
        default=os.getenv(
            'ID_FIELD_NAME',
            None,
        ),
    )
    parser.add_argument(
        '--update_field_names',
        help='BigQuery table name (endpoint)',
        default=os.getenv(
            'UPDATE_FIELD_NAMES',
            None,
        ),
    )
    args = parser.parse_args()

    main(
        project_id=args.project_id,
        db_name=args.db_name,
        table_name=args.table_name,
        dtype_dict=eval(args.dtype_dict),
        id_field_names=args.id_field_names.split(" "),
        update_field_names=args.update_field_names.split(" "),
    )
