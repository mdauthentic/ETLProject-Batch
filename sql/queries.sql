
CREATE TABLE IF NOT EXISTS jobs (
    id SERIAL PRIMARY KEY,
    job_id INTEGER NOT NULL REFERENCES jobs (id),
    title VARCHAR(255) NOT NULL,
    description TEXT NOT NULL
    date_created TIMESTAMP NOT NULL
);

CREATE TABLE IF NOT EXISTS jobs_info (
    id SERIAL PRIMARY KEY,
    job_id INTEGER NOT NULL REFERENCES jobs (id),
    contract_type VARCHAR(55) NOT NULL,
    seniority_level VARCHAR(255) NOT NULL,
    date_posted TIMESTAMP NOT NULL
);

CREATE TABLE IF NOT EXISTS company (
    id SERIAL NOT NULL PRIMARY KEY,
    name VARCHAR(30) NOT NULL,
    location VARCHAR(40) NOT NULL
);

CREATE TABLE salary (
    id SERIAL NOT NULL PRIMARY KEY,
    job_id INTEGER NOT NULL REFERENCES jobs (id),
    salary_range VARCHAR(20) NOT NULL,
    salary_unit VARCHAR(7) NOT NULL
);

CREATE TABLE job_tags (
    id SERIAL NOT NULL PRIMARY KEY,
    job_id INTEGER NOT NULL REFERENCES jobs (id),
    post_tag VARCHAR(10) NOT NULL
);

CREATE TABLE daily_word_count (
    id SERIAL NOT NULL PRIMARY KEY,
    job_id INTEGER NOT NULL REFERENCES jobs (id),
    word_count INTEGER(10) NOT NULL,
    date_created TIMESTAMP NOT NULL
);

CREATE TABLE job_word_count (
    id SERIAL NOT NULL PRIMARY KEY,
    job_id INTEGER NOT NULL REFERENCES jobs (id),
    topn_words INTEGER(10) NOT NULL,
    date_created TIMESTAMP NOT NULL
);

CREATE TABLE github_trends (
    id SERIAL NOT NULL PRIMARY KEY,
    repository VARCHAR(55) NOT NULL,
    repo_url TEXT NOT NULL,
    date_created TIMESTAMP NOT NULL
);