from db import db
from sqlalchemy.sql import text
from werkzeug.security import check_password_hash, generate_password_hash

def check_credentials(username, password):
    result = db.session.execute(text("SELECT id, password_hash FROM users WHERE username=:username"), {"username":username})
    user = result.fetchone()    
    if not user:
        return False
    else:
        if check_password_hash(user.password_hash, password):
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
    

