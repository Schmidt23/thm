#!/usr/bin/env python3

import os
import yaml
from functools import wraps
from flask import (
    Flask, render_template, request, redirect,
    url_for, session, flash, Response,
)

app = Flask(__name__)
app.secret_key = "beach-bar-jukebox-fixed-session-key"

USERS = {
    "dj": "dj",
}

SAMPLE_PLAYLIST = """\
# Beach Bar jukebox playlist export
playlist:
  name: Sunset Session
  vibe: golden hour
  tracks:
    - artist: Khruangbin
      title: Maria Tambien
    - artist: Men I Trust
      title: Show Me How
    - artist: Crumb
      title: Locket
"""


def login_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if not session.get("user"):
            return redirect(url_for("login"))
        return f(*args, **kwargs)
    return wrapper


@app.route("/")
def index():
    if session.get("user"):
        return redirect(url_for("dashboard"))
    return redirect(url_for("login"))


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        u = request.form.get("username", "")
        p = request.form.get("password", "")
        if USERS.get(u) == p:
            session["user"] = u
            return redirect(url_for("dashboard"))
        flash("Invalid credentials.")
    return render_template("login.html")


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


@app.route("/dashboard")
@login_required
def dashboard():
    return render_template("dashboard.html", user=session["user"])


@app.route("/export")
@login_required
def export():
    return Response(
        SAMPLE_PLAYLIST,
        mimetype="application/x-yaml",
        headers={"Content-Disposition": "attachment; filename=playlist.yml"},
    )


@app.route("/import", methods=["GET", "POST"])
@login_required
def import_playlist():
    result = None
    error = None
    if request.method == "POST":
        content = request.form.get("playlist", "")
        if "playlist_file" in request.files:
            f = request.files["playlist_file"]
            if f and f.filename:
                content = f.read().decode("utf-8", "replace")
        try:
            parsed = yaml.load(content, Loader=yaml.Loader)
            result = parsed
        except Exception as e:
            error = f"Could not load playlist: {e}"
    return render_template("import.html", result=result, error=error)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)
