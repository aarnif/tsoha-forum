from db import db
from sqlalchemy.sql import text
from werkzeug.security import check_password_hash, generate_password_hash
from flask import session

def get_user(username):
    result = db.session.execute(text("SELECT id, username, password_hash, role FROM users WHERE username=:username"), {"username":username})
    user = result.fetchone()
    return user

def get_all_basic_users():
    result = db.session.execute(text("SELECT id, username, role FROM users WHERE role=0"))
    users = result.fetchall()
    return users

def logout():
    del session["user_id"]
    del session["username"]
    del session["role"]

def login(username, password):
    user = get_user(username)
    if user and check_password_hash(user.password_hash, password):
        session["user_id"] = user.id
        session["username"] = user.username
        session["role"] = user.role
        return True
    else:
        return False
        
def check_if_user_exists(username):
    result = db.session.execute(text("SELECT id FROM users WHERE username=:username"), {"username":username})
    user = result.fetchone()
    if user:
        return True
    else:
        return False
        
def create_user(username, password, role):
    password_hash = generate_password_hash(password)
    try:
        db.session.execute(text("INSERT INTO users (username, password_hash, role) \
                                 VALUES (:username, :password_hash, :role)"), 
                           {"username":username, "password_hash":password_hash, "role":role})
        db.session.commit()
        return True
    except:
        print("Error creating user")
        return False
    

