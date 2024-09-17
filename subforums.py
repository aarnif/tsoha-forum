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
    result = db.session.execute(text("SELECT sf.id as sf_id, t.creator_id as t_creator_id, t.id AS t_id, t.title AS title, COUNT(m.id) AS messages, \
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
                                     username, m.content AS content, m.created_at AS created_at, m.updated_at AS updated_at \
                                    FROM \
                                        threads t LEFT JOIN messages m ON m.thread_id = t.id \
                                    LEFT JOIN users u ON m.creator_id = u.id \
                                    WHERE t.id = :thread_id ORDER BY created_at"), {"thread_id": thread_id})
    thread = result.fetchall()
    return thread

def create_thread(subforum_id, user_id, title, message_content):
    try:
        db.session.execute(text("INSERT INTO threads (subforum_id, creator_id, title) \
                                VALUES (:subforum_id, :creator_id, :title)"), \
                                {"subforum_id": subforum_id, "creator_id": user_id, "title": title})
        db.session.commit()
        thread_id = db.session.execute(text("SELECT id FROM threads WHERE subforum_id = :subforum_id AND creator_id = :creator_id AND title = :title"), \
                                        {"subforum_id": subforum_id, "creator_id": user_id, "title": title}).fetchone()[0]
        add_message_to_thread(thread_id, user_id, message_content)
        return True
    except:
        print("Error creating thread")
        return False
    
def update_thread(thread_id, title):
    try:
        db.session.execute(text("UPDATE threads SET title = :title, updated_at = Now() WHERE id = :thread_id"), {"title": title, "thread_id": thread_id})
        db.session.commit()
        return True
    except:
        print("Error updating thread")
        return False
    
def delete_thread(thread_id):
    try:
        db.session.execute(text("DELETE FROM threads WHERE id = :thread_id"), {"thread_id": thread_id})
        db.session.commit()
        return True
    except:
        print("Error deleting thread")
        return False
   

def add_message_to_thread(thread_id, user_id, message_content):
    try:
        db.session.execute(text("INSERT INTO messages (thread_id, creator_id, content) \
                                VALUES (:thread_id, :creator_id, :content)"), \
                                {"thread_id": thread_id, "creator_id": user_id, "content": message_content})
        db.session.commit()
        return True
    except:
        print("Error adding message")
        return False

def get_message(message_id):
    result = db.session.execute(text("SELECT id, thread_id, creator_id, content, created_at, updated_at \
                                     FROM messages WHERE id = :message_id"), {"message_id": message_id})
    message = result.fetchone()
    return message

def update_message(message_id, message_content):
    try:
        db.session.execute(text("UPDATE messages SET content = :content, updated_at = Now() \
                                WHERE id = :message_id"), {"content": message_content, "message_id": message_id})
        db.session.commit()
        return True
    except:
        print("Error updating message")
        return False


def delete_message(message_id):
    try:
        db.session.execute(text("DELETE FROM messages WHERE id = :message_id"), {"message_id": message_id})
        db.session.commit()
        return True
    except:
        print("Error deleting message")
        return False