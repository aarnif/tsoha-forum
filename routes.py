from flask import render_template, request, session, redirect
from app import app
import users
import subforums

@app.route("/")
def index():
    if session.get("username"):
        all_subforums = subforums.get_all_subforums()
        secret_subforums = []
        if session.get("role") == 1:
            secret_subforums = subforums.get_all_secret_subforums()
        else:
            secret_subforums = subforums.get_all_secret_subforums_by_user(session["user_id"])
        return render_template("index.html", all_subforums=all_subforums,
secret_subforums=secret_subforums)

    return redirect("/login")

# User routes
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")

    username = request.form["username"]
    if len(username) < 4 or len(username) > 20:
        return render_template("register.html", message="Tunnuksen tulee olla 4-20 merkkiä pitkä!")

    if users.check_if_user_exists(username):
        return render_template("register.html", message="Käyttäjätunnus on jo käytössä!")

    password = request.form["password"]
    confirm_password = request.form["confirm-password"]
    role = request.form["role"]

    if len(password) < 6:
        return render_template("register.html",
message="Salasanan tulee olla vähintään 6 merkkiä pitkä!")

    if password != confirm_password:
        return render_template("register.html", message="Salasanat eivät täsmää!")

    if not users.create_user(username, password, role):
        return render_template("register.html",
message="Rekisteröinti ei onnistunut! Ole hyvä ja yritä uudelleen.")

    users.login(username, password)

    return redirect("/")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")

    username = request.form["username"]
    password = request.form["password"]
    if not users.login(username, password):
        return render_template("login.html", message="Väärä käyttäjätunnus tai salasana!")

    return redirect("/")

@app.route("/logout")
def logout():
    users.logout()
    return redirect("/login")


# Sub forum routes
@app.route("/subforums/<int:subforum_id>")
def sub_forum(subforum_id):
    subforum = subforums.get_subforum(subforum_id)
    return render_template("subforum.html", subforum=subforum)

@app.route("/subforums/new", methods=["GET", "POST"])
def new_subforum_post():
    if request.method == "GET":
        basic_users = users.get_all_basic_users()
        return render_template("new_subforum.html", basic_users=basic_users)

    name = request.form["name"]
    description = request.form["description"]
    is_secret = request.form["is-secret"]
    users_with_access = request.form.getlist("users")

    if len(name) < 6 or len(name) > 30:
        return render_template("new_subforum.html", message="Nimen tulee olla 6-30 merkkiä pitkä!")

    if not subforums.create_subforum(name, description, is_secret, users_with_access):
        return render_template("new_subforum.html",
message="Virhe luotaessa uutta aluealuetta! Ole hyvä ja yritä uudelleen.")

    return redirect("/")

@app.route("/subforums/<int:subforum_id>/delete", methods=["GET", "POST"])
def delete_subforum(subforum_id):
    if request.method == "GET":
        subforum = subforums.get_subforum(subforum_id)
        return render_template("delete_subforum.html", subforum=subforum)

    subforums.delete_subforum(subforum_id)
    return redirect("/")


# Thread routes
@app.route("/subforums/<int:sub_forum_id>/threads/<int:thread_id>", methods=["GET", "POST"])
def thread(sub_forum_id, thread_id):
    if request.method == "POST":
        message_content = request.form["message-content"]
        subforums.add_message_to_thread(thread_id, session["user_id"], message_content)
    thread = subforums.get_thread(thread_id)
    return render_template("thread.html", thread=thread, return_url= f"/subforums/{sub_forum_id}")

@app.route("/subforums/<int:sub_forum_id>/threads/new", methods=["GET", "POST"])
def new_thread(sub_forum_id):
    if request.method == "GET":
        return render_template("new_thread.html", return_url=f"/subforums/{sub_forum_id}")

    title = request.form["title"]
    message_content = request.form["message-content"]

    if len(title) < 6 or len(title) > 30:
        return render_template("new_thread.html", message="Otsikon tulee olla 6-30 merkkiä pitkä!")

    if len(message_content) < 1:
        return render_template("new_thread.html", message="Viesti ei voi olla tyhjä!")

    if not subforums.create_thread(sub_forum_id, session["user_id"], title, message_content):
        return render_template("new_thread.html",
message="Virhe luotaessa uutta ketjua! Ole hyvä ja yritä uudelleen.")

    return redirect(f"/subforums/{sub_forum_id}")

@app.route("/subforums/<int:sub_forum_id>/threads/<int:thread_id>/update", methods=["GET", "POST"])
def update_thread(sub_forum_id, thread_id):
    return_url=f"/subforums/{sub_forum_id}"
    thread = subforums.get_thread(thread_id)

    if request.method == "GET":
        return render_template("update_thread.html",
thread=thread, return_url=return_url, message="")

    title = request.form["title"]

    if len(title) < 6 or len(title) > 30:
        return render_template("update_thread.html", thread=thread,
return_url=return_url, message="Otsikon tulee olla 6-30 merkkiä pitkä!")

    if not subforums.update_thread(thread_id, title):
        return render_template("update_thread.html", thread=thread,
return_url=return_url, message="Virhe päivittäessa ketjua! Ole hyvä ja yritä uudelleen.")

    return redirect(f"/subforums/{sub_forum_id}")

@app.route("/subforums/<int:sub_forum_id>/threads/<int:thread_id>/delete", methods=["GET", "POST"])
def delete_thread_post(sub_forum_id, thread_id):
    if request.method == "GET":
        thread = subforums.get_thread(thread_id)
        return render_template("delete_thread.html", thread=thread,
return_url=f"/subforums/{sub_forum_id}")

    subforums.delete_thread(thread_id)
    return redirect(f"/subforums/{sub_forum_id}")


# Message routes
@app.route("/subforums/<int:sub_forum_id>/threads/<int:thread_id>/messages/<int:message_id>/update",
methods=["GET", "POST"])
def update_message_post(sub_forum_id, thread_id, message_id):
    if request.method == "GET":
        message = subforums.get_message(message_id)
        return render_template("update_message.html", message=message,
return_url=f"/subforums/{sub_forum_id}/threads/{thread_id}")

    message_content = request.form["message-content"]
    subforums.update_message(message_id, message_content)
    return redirect(f"/subforums/{sub_forum_id}/threads/{thread_id}")

@app.route("/subforums/<int:sub_forum_id>/threads/<int:thread_id>/messages/<int:message_id>/delete",
methods=["GET", "POST"])
def delete_message_post(sub_forum_id, thread_id, message_id):
    if request.method == "GET":
        message = subforums.get_message(message_id)
        return render_template("delete_message.html", message=message,
return_url=f"/subforums/{sub_forum_id}/threads/{thread_id}")

    subforums.delete_message(message_id)
    return redirect(f"/subforums/{sub_forum_id}/threads/{thread_id}")

# Search messages route
@app.route("/result")
def result():
    search_word = request.args["search-word"]
    messages = subforums.search_messages(search_word)
    return render_template("result.html", messages=messages)
