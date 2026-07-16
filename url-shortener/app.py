"""
URL Shortener
-------------
A Flask web app that converts long URLs into short, shareable links.
Uses SQLite for storage and redirects visitors from the short link to the
original URL.

Usage:
    python app.py
    Then open http://127.0.0.1:5000 in your browser.
"""

import sqlite3
import string
import secrets
from urllib.parse import urlparse

from flask import Flask, render_template, request, redirect, url_for, abort

app = Flask(__name__)
DB_FILE = "urls.db"
CODE_LENGTH = 6


def get_db():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db()
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS urls (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            original_url TEXT NOT NULL,
            short_code TEXT UNIQUE NOT NULL,
            clicks INTEGER DEFAULT 0
        )
        """
    )
    conn.commit()
    conn.close()


def generate_short_code(conn) -> str:
    alphabet = string.ascii_letters + string.digits
    while True:
        code = "".join(secrets.choice(alphabet) for _ in range(CODE_LENGTH))
        existing = conn.execute(
            "SELECT 1 FROM urls WHERE short_code = ?", (code,)
        ).fetchone()
        if not existing:
            return code


def is_valid_url(url: str) -> bool:
    try:
        result = urlparse(url)
        return all([result.scheme in ("http", "https"), result.netloc])
    except ValueError:
        return False


@app.route("/", methods=["GET", "POST"])
def index():
    error = None
    short_url = None

    if request.method == "POST":
        original_url = request.form.get("url", "").strip()

        if not is_valid_url(original_url):
            error = "Please enter a valid URL starting with http:// or https://"
        else:
            conn = get_db()
            existing = conn.execute(
                "SELECT short_code FROM urls WHERE original_url = ?", (original_url,)
            ).fetchone()
            if existing:
                code = existing["short_code"]
            else:
                code = generate_short_code(conn)
                conn.execute(
                    "INSERT INTO urls (original_url, short_code) VALUES (?, ?)",
                    (original_url, code),
                )
                conn.commit()
            conn.close()
            short_url = url_for("redirect_to_original", code=code, _external=True)

    conn = get_db()
    links = conn.execute(
        "SELECT original_url, short_code, clicks FROM urls ORDER BY id DESC LIMIT 10"
    ).fetchall()
    conn.close()

    return render_template("index.html", error=error, short_url=short_url, links=links)


@app.route("/<code>")
def redirect_to_original(code):
    conn = get_db()
    row = conn.execute(
        "SELECT original_url FROM urls WHERE short_code = ?", (code,)
    ).fetchone()
    if row is None:
        conn.close()
        abort(404)
    conn.execute(
        "UPDATE urls SET clicks = clicks + 1 WHERE short_code = ?", (code,)
    )
    conn.commit()
    conn.close()
    return redirect(row["original_url"])


if __name__ == "__main__":
    init_db()
    app.run(debug=True)
