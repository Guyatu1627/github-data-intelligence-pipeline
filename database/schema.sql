CREATE TABLE repositories (
    id SERIAL PRIMARY KEY,
    repo_name TEXT,
    stars INTEGER,
    forks INTEGER,
    open_issues INTEGER,
    collected_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE contributors (
    id SERIAL PRIMARY KEY,
    repo_name TEXT,
    contributors_login TEXT,
    contributions INTEGER
);

CREATE TABLE commits (
    id SERIAL PRIMARY KEY,
    repo_name TEXT,
    commit_sha TEXT,
    author_login TEXT,
    commit_message TEXT,
    commit_date TIMESTAMP 
);

CREATE INDEX idx_repo_name ON contributors(repo_name);
CREATE INDEX idx_commit_repo ON commits(repo_name);