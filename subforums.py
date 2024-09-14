from db import db
from sqlalchemy.sql import text

def get_all_subforums():
    result = db.session.execute(text("SELECT sf.id as id, sf.name AS name, sf.description AS description, COUNT(DISTINCT t.id) AS threads, \
                                COUNT(m.id) AS messages, MAX(m.created_at) AS lastest_message \
                                FROM subforums sf \
                                LEFT JOIN threads t ON sf.id = t.subforum_id \
                                LEFT JOIN messages m ON t.id = m.thread_id \
                                WHERE is_secret = FALSE \
                                GROUP BY sf.id, sf.name"))
    subforums = result.fetchall()
    return subforums

def get_subforum(subforum_id):
    result = db.session.execute(text("SELECT sf.id as sf_id, t.id AS t_id, t.title AS title, COUNT(m.id) AS messages, \
                                    MAX(m.created_at) AS lastest_message \
                                    FROM \
                                        subforums sf LEFT JOIN threads t ON sf.id = t.subforum_id \
                                        LEFT JOIN messages m ON t.id = m.thread_id \
                                        WHERE sf.id = :subforum_id \
                                    GROUP BY sf.id, t.id, t.title"), {"subforum_id": subforum_id})
    subforum = result.fetchall()
    return subforum

def get_thread(thread_id):
    result = db.session.execute(text("SELECT t.id as t_id, t.title AS title, m.id AS m_id, \
                                     username, m.content AS content, m.created_at AS created_at \
                                    FROM \
                                        threads t LEFT JOIN messages m ON m.thread_id = t.id \
                                    LEFT JOIN users u ON m.creator_id = u.id \
                                    WHERE t.id = :thread_id"), {"thread_id": thread_id})
    thread = result.fetchall()
    return thread