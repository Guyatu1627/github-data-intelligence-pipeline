from fastapi import FastAPI
import psycopg2

app = FastAPI()

DB_CONFIG = {
    "host": "localhost",
    "database": "github_analytics",
    "user": "postgres",
    "password": "postgres@2025"
}


def connect():
    return psycopg2.connect(**DB_CONFIG)


@app.get("/top-contributors")
def top_contributors():
    conn = connect()
    cur = conn.cursor()

    cur.execute(
        """
        SELECT contributor_login, SUM(contributions) as total
        FROM contributors
        GROUP BY contributor_login
        ORDER BY total DESC
        LIMIT 10
        """
    )

    data = cur.fetchall()

    return {"contributors": data}


@app.get("/repo-stats")
def repo_stats():
    conn = connect()
    cur = conn.cursor()

    cur.execute(
        """
        SELECT repo_name, stars, forks, open_issues
        FROM repositories
        ORDER BY collected_at DESC
        LIMIT 1
        """
    )

    data = cur.fetchone()

    return {"repo": data}