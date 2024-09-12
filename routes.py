from app import app


@app.route("/")
def index():
    return "The main page, NOT IMPLEMENTED YET!"

# User routes
@app.route("/register", methods=["GET", "POST"])
def register():
    return "User registration page, NOT IMPLEMENTED YET!"

@app.route("/login", methods=["GET", "POST"])
def login():
    return "User login page, NOT IMPLEMENTED YET!"

@app.route("/logout")
def logout():
    return "User logout, NOT IMPLEMENTED YET!"

# Sub forum routes
@app.route("/sub_forums")
def sub_forums():
    return "The sub-forums page, NOT IMPLEMENTED YET!"

@app.route("/sub_forums/<int:sub_forum_id>")
def sub_forum(sub_forum_id):
    return f"The sub-forum {sub_forum_id}, NOT IMPLEMENTED YET!"

# Thread routes
@app.route("/sub_forums/<int:sub_forum_id>/threads")
def threads(sub_forum_id):
    return f"The sub-forum {sub_forum_id} threads, NOT IMPLEMENTED YET!"

@app.route("/sub_forums/<int:sub_forum_id>/threads/<int:thread_id>")
def thread(sub_forum_id, thread_id):
    return f"The individual thread {thread_id} in sub-forum {sub_forum_id}, NOT IMPLEMENTED YET!"