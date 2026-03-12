import psycopg2
import pandas as pd

DB_CONFIG = {
    "host": "localhost",
    "database": "github_analytics",
    "user": "postgres",
    "password": "postgres@2025"
}


def connect():
    return psycopg2.connect(**DB_CONFIG)


def compute_top_contributors():
    conn = connect()

    query = """
    SELECT contributor_login, SUM(contributions) as total_contributions
    FROM contributors
    GROUP BY contributor_login
    ORDER BY total_contributions DESC
    """

    df = pd.read_sql(query, conn)

    print(df.head())


if __name__ == "__main__":
    compute_top_contributors()