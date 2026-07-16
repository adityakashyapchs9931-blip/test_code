# URL Shortener

A small Flask web app that converts long URLs into short, shareable links
and redirects visitors back to the original page.

## Features

- Clean web UI to submit a URL and get a short link instantly.
- Short codes generated with Python's `secrets` module (not guessable).
- SQLite database (`urls.db`) stores the mapping between short codes and original URLs.
- Click tracking — see how many times each short link has been visited.
- Re-submitting the same URL returns the existing short link instead of creating a duplicate.

## Usage

```bash
pip install -r requirements.txt
python app.py
```

Then open **http://127.0.0.1:5000** in your browser.

## How it works

1. You paste a long URL into the form.
2. The app generates a random 6-character code and stores `original_url -> code` in SQLite.
3. Visiting `http://127.0.0.1:5000/<code>` looks up the original URL and redirects you there.

## Project structure

```
url-shortener/
  app.py              # Flask app + routes + database logic
  templates/
    index.html         # Web UI
  requirements.txt
  urls.db              # created automatically on first run (not committed)
```
