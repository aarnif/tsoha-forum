from app import app
from flask import render_template, request, session, redirect
import users

@app.route("/")
def index():
    if session.get("username"):
        return render_template("index.html")
    
    return redirect("/login")

# User routes
@app.route("/register", methods=["GET", "POST"])
def register():
    return "User registration page, NOT IMPLEMENTED YET!"

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