import requests
import psycopg2

DB_CONFIG = {
    "host": "localhost",
    "database": "github_analytics",
    "user": "postgres",
    "password": "postgres@2025"
}

REPO = "pandas-dev/pandas"


def connect_db():
    return psycopg2.connect(**DB_CONFIG)


def fetch_repo_info():
    url = f"https://api.github.com/repos/{REPO}"
    response = requests.get(url)
    return response.json()


def fetch_contributors():
    url = f"https://api.github.com/repos/{REPO}/contributors"
    response = requests.get(url)
    return response.json()


def fetch_commits():
    url = f"https://api.github.com/repos/{REPO}/commits"
    response = requests.get(url)
    return response.json()


def store_repository(data):
    conn = connect_db()
    cur = conn.cursor()

    cur.execute(
        """
        INSERT INTO repositories(repo_name, stars, forks, open_issues)
        VALUES (%s, %s, %s, %s)
        """,
        (
            data["full_name"],
            data["stargazers_count"],
            data["forks_count"],
            data["open_issues_count"],
        ),
    )

    conn.commit()
    cur.close()
    conn.close()


def store_contributors(data):
    conn = connect_db()
    cur = conn.cursor()

    for c in data:
        cur.execute(
            """
            INSERT INTO contributors(repo_name, contributor_login, contributions)
            VALUES (%s, %s, %s)
            """,
            (REPO, c["login"], c["contributions"]),
        )

    conn.commit()
    cur.close()
    conn.close()


def store_commits(data):
    conn = connect_db()
    cur = conn.cursor()

    for c in data:
        commit = c["commit"]

        cur.execute(
            """
            INSERT INTO commits(repo_name, commit_sha, author_login, commit_message, commit_date)
            VALUES (%s, %s, %s, %s, %s)
            """,
            (
                REPO,
                c["sha"],
                commit["author"]["name"],
                commit["message"],
                commit["author"]["date"],
            ),
        )

    conn.commit()
    cur.close()
    conn.close()


def run_pipeline():
    repo = fetch_repo_info()
    contributors = fetch_contributors()
    commits = fetch_commits()

    store_repository(repo)
    store_contributors(contributors)
    store_commits(commits)


if __name__ == "__main__":
    run_pipeline()
