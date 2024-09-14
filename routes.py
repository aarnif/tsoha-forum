from app import app
from flask import render_template, request, session, redirect
import users
import subforums

@app.route("/")
def index():
    if session.get("username"):
        all_subforums = subforums.get_all_subforums()
        print("Subforums:", all_subforums)
        return render_template("index.html", all_subforums=all_subforums)
    
    return redirect("/login")

# User routes
@app.route("/register", methods=["GET"])
def register_get():
    return render_template("register.html")

@app.route("/register", methods=["POST"])
def register_post():
    username = request.form["username"]
    if len(username) < 4 or len(username) > 20:
        return render_template("register.html", message="Tunnuksen tulee olla 4-20 merkkiä pitkä!")
    
    if users.check_if_user_exists(username):
        return render_template("register.html", message="Käyttäjätunnus on jo käytössä!")

    password = request.form["password"]
    confirm_password = request.form["confirm-password"]
    role = request.form["role"]

    if len(password) < 6:
        return render_template("register.html", message="Salasanan tulee olla vähintään 6 merkkiä pitkä!")
    
    if password != confirm_password:
        return render_template("register.html", message="Salasanat eivät täsmää!")

    if not users.create_user(username, password, role):
        return render_template("register.html", message="Rekisteröinti ei onnistunut! Ole hyvä ja yritä uudelleen.")
    
    session["username"] = username
    return redirect("/")

@app.route("/login", methods=["GET"])
def login_get():
    return render_template("login.html")

@app.route("/login", methods=["POST"])
def login_post():
    username = request.form["username"]
    password = request.form["password"]
    if not users.check_credentials(username, password):
        return render_template("login.html", message="Väärä käyttäjätunnus tai salasana!")

    session["username"] = username
    return redirect("/")

@app.route("/logout")
def logout():
    del session["username"]
    return redirect("/login")

# Sub forum routes
@app.route("/subforums/<int:subforum_id>")
def sub_forum(subforum_id):
    print("Subforum ID:", subforum_id)
    subforum = subforums.get_subforum(subforum_id)
    print("Subforum:", subforum)
    return render_template("subforum.html", subforum=subforum)

# Thread routes
@app.route("/subforums/<int:sub_forum_id>/threads")
def threads(sub_forum_id):
    return f"The sub-forum {sub_forum_id} threads, NOT IMPLEMENTED YET!"

@app.route("/subforums/<int:sub_forum_id>/threads/<int:thread_id>")
def thread(sub_forum_id, thread_id):
    return f"The individual thread {thread_id} in sub-forum {sub_forum_id}, NOT IMPLEMENTED YET!"