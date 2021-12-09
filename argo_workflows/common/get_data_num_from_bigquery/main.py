import os
import argparse
from google.cloud import bigquery


def main(
    project_id: str,
    db_name: str,
    table_name: str,
    id_field_name: str,
    where: str = None,
    group_by: str = None,
):
    """Print the number of data selected from specified database.

    :param project_id: Name of GCP project that has database
    :type project_id: str
    :param db_name: Name of BigQuery database
    :type db_name: str
    :param table_name: Table name of BigQuery database
    :type table_name: str
    :param id_field_name: Id field name in the table
    :type id_field_name: str
    :param where: Select option
    :type where: str
    :param group_by: Select option
    :type group_by: str

    """
    client = bigquery.Client()
    query = f"""
    SELECT
        count({id_field_name}) as data_num
    FROM
        `{project_id}.{db_name}.{table_name}`
    """
    if where:
        query += f"""
        WHERE
            {where}
        """.lstrip()

    query_job = client.query(query)
    result = (
        query_job
        .result()
        .to_dataframe()
    )
    print(result["data_num"][0])

    return


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--project_id',
        help='BigQuery table name (endpoint)',
        required=True,
    )
    parser.add_argument(
        '--db_name',
        help='BigQuery table name (endpoint)',
        required=True,
    )
    parser.add_argument(
        '--table_name',
        help='BigQuery table name (endpoint)',
        required=True,
    )
    parser.add_argument(
        '--id_field_name',
        help='BigQuery table name (endpoint)',
        required=True,
    )
    parser.add_argument(
        '--where',
        help='BigQuery table name (endpoint)',
        default=os.getenv('WHERE', None),
    )
    args = parser.parse_args()

    main(
        project_id=args.project_id,
        db_name=args.db_name,
        table_name=args.table_name,
        id_field_name=args.id_field_name,
        where=args.where,
    )
