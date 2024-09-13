from db import db
from sqlalchemy.sql import text
from werkzeug.security import check_password_hash

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