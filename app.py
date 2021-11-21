from flask import Flask, render_template, session, redirect, Response, request, g
from passlib.hash import pbkdf2_sha256
import config
import api
import database
import subprocess
import time

thumbs = {}
database.Initialize()




app = Flask(__name__)
app.config["SECRET_KEY"] = config.key

@app.after_request
def add_header(r):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    r.headers['Cache-Control'] = 'public, max-age=0'
    return r

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

@app.context_processor
def LoadGlobals():
    return {
        "SITENAME": config.sitename,
        "HOSTNAME": config.hostname,
        "RTMPURL": config.rtmpurl,
        "HLSURL": config.hlsurl
    }

@app.route('/account', methods=["GET", "POST"])
def account():
    if "user" in session:
        acct = database.GetAccount(session["user"])
        title_error = ""
        if request.method == "POST":
            form = request.form
            title = acct["title"]
            hidden = acct["hidden"]
            if form.get("title", ""):
                if len(form["title"]) > 250:
                    title_error = "Title must be 250 characters or less."
                else:
                    title = form["title"]
            if form.get("visibility", None) in ("0", "1"):
                hidden = form["visibility"]
            database.UpdateAccount(session["user"], title, hidden)
            acct = database.GetAccount(session["user"])
        return render_template("account.html", account=acct, title_error=title_error)
    else:
        return redirect("/login", 302)

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/", 302)

@app.route("/login", methods=["GET", "POST"])
def login():
    login_error = ""
    register_error = ""
    if request.method == "POST":
        form = request.form
        if form.get("type", None) == "login" and form.get("username", None) and form.get("password", None):
            acct = database.GetAccount(form["username"])
            if not acct:
                login_error = "Account not found."
            else:
                if not pbkdf2_sha256.verify(form["password"], acct["password"]):
                    login_error = "Password incorrect"
                else:
                    session["user"] = acct["username"]
                    return redirect("/", 302)
        elif form.get("type", None) == "register" and form.get("username", None):
            acct = database.GetAccount(form["username"])
            if acct:
                register_error = "Account already exists."
            else:
                validations = [
                    bool(form.get("password", False)),
                    form["username"].isalnum(),
                    len(form["username"]) > 2,
                    len(form["username"]) <= 20,
                    len(form["password"]) > 5,
                    len(form["password"]) <= 128,
                    form["password"] == form["password-confirm"],
                    bool(database.HasToken(form.get("invite", "-")))
                ]
                messages = [
                    "You need a password.",
                    "Usernames must be alphanumeric",
                    "Usernames must be at least 3 characters",
                    "Usernames must be 20 characters or less",
                    "Passwords must be 6 characters or more",
                    "Passwords must be 128 characters or less",
                    "Passwords do not match.",
                    "Invalid invite."
                ]
                if all(validations):
                    database.CreateAccount(form["username"], form["password"])
                    database.RemoveToken(form.get("invite", "-"))
                    session["user"] = form["username"]
                    return redirect("/", 302)
                else:
                    register_error = messages[validations.index(False)]

    return render_template("login.html", login_error=login_error, register_error=register_error)

@app.route("/s/<user>")
def stream(user):
    return render_template("stream.html", path=user, active=api.IsPathActive(user), info=database.GetAccount(user))


@app.route("/thumb/<path>.jpg")
def thumbnail(path):
    if path not in thumbs or thumbs[path][1] < time.time():
        proc = subprocess.Popen(["ffmpeg", "-hide_banner", "-loglevel", "quiet", "-i", f"http://localhost:8888/{path}/stream.m3u8", "-vframes", '1', '-vf', "scale=320:-1", "-f", "image2", "-"],
                                stdout=subprocess.PIPE)
        thumbs[path] = (proc.communicate()[0], time.time()+60)
    return Response(thumbs[path][0], mimetype="image/jpeg")


@app.route('/about')
def about():
    return render_template("about.html")

@app.route('/')
def index():
    streaming = api.GetAllStreaming()
    return render_template("index.html", streaming=streaming)



if __name__ == '__main__':
    app.run()
