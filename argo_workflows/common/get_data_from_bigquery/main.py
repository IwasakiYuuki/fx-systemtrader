import os
import argparse
from google.cloud import bigquery


def main(
    project_id: str,
    db_name: str,
    table_name: str,
    where: str = None,
    group_by: str = None,
    limit: str = None,
    offset: str = None,
):
    """Save the data selected from specified BigQuery database to local file.

    The local file name is '/tmp/output.csv'.

    :param project_id: Name of GCP project that has database
    :type project_id: str
    :param db_name: Name of BigQuery database
    :type db_name: str
    :param table_name: Table name of BigQuery database
    :type table_name: str
    :param where: Select option
    :type where: str
    :param group_by: Select option
    :type group_by: str
    :param limit: Select option
    :type limit: str
    :param offset: Select option
    :type offset: str

    """
    client = bigquery.Client()
    query = f"""
    SELECT
        *
    FROM
        `{project_id}.{db_name}.{table_name}`
    """
    if where:
        query += f"""
        WHERE
            {where}
        """.lstrip()
    if group_by:
        query += f"""
        GROUP BY
            {group_by}
        """.lstrip()
    if limit:
        query += f"""
        LIMIT
            {limit}
        """.lstrip()
    if offset:
        query += f"""
        OFFSET
            {offset}
        """.lstrip()

    query_job = client.query(query)
    result = (
        query_job
        .result()
        .to_dataframe()
    )
    print(result.shape[0])
    result.to_csv("/tmp/output.csv", index=False)

    return


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--project_id',
        help='GCP Project id',
        required=True,
    )
    parser.add_argument(
        '--db_name',
        help='Target DB name in BigQuery',
        required=True,
    )
    parser.add_argument(
        '--table_name',
        help='Target table name in BigQuery',
        required=True,
    )
    parser.add_argument(
        '--where',
        help=(
            'SQL query condition.'
            'If not got this, '
            'use value of environment variable WHERE by default.',
        ),
        default=os.getenv(
            'WHERE',
            None),
    )
    parser.add_argument(
        '--group_by',
        help=(
            'SQL query condition.'
            'If not got this, '
            'use value of environment variable GROUP_BY by default.',
        ),
        default=os.getenv(
            'GROUP_BY',
            None),
    )
    parser.add_argument(
        '--limit',
        help=(
            'SQL query condition.'
            'If not got this, '
            'use value of environment variable LIMIT by default.',
        ),
        default=os.getenv(
            'LIMIT',
            None),
    )
    parser.add_argument(
        '--offset',
        help=(
            'SQL query condition.'
            'If not got this, '
            'use value of environment variable OFFSET by default.',
        ),
        default=os.getenv(
            'OFFSET',
            None),
    )
    args = parser.parse_args()

    main(
        project_id=args.project_id,
        db_name=args.db_name,
        table_name=args.table_name,
        where=args.where,
        group_by=args.group_by,
        limit=args.limit,
        offset=args.offset,
    )
