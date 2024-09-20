CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username TEXT UNIQUE,
    password_hash TEXT,
    role INTEGER
);

CREATE TABLE subforums (
    id SERIAL PRIMARY KEY,
    creator_id INTEGER REFERENCES users,
    name TEXT,
    description TEXT,
    is_secret BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE subforum_access (
    id SERIAL PRIMARY KEY,
    subforum_id INTEGER REFERENCES subforums ON DELETE CASCADE,
    user_id INTEGER REFERENCES users
);

CREATE TABLE threads (
    id SERIAL PRIMARY KEY,
    subforum_id INTEGER REFERENCES subforums ON DELETE CASCADE,
    creator_id INTEGER REFERENCES users,
    title TEXT,
    subtitle TEXT,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE messages (
    id SERIAL PRIMARY KEY,
    thread_id INTEGER REFERENCES threads ON DELETE CASCADE,
    creator_id INTEGER REFERENCES users,
    content TEXT,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);