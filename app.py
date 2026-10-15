import os
import secrets
import socket

import redis
from flask import Flask, jsonify, redirect, request

app = Flask(__name__)
db = redis.Redis(host=os.getenv("REDIS_HOST", "redis"), port=6379, decode_responses=True)


@app.get("/")
def index():
    """Shows which container answered, to prove the load balancing works."""
    return jsonify(
        served_by=socket.gethostname(),
        total_requests=db.incr("stats:requests"),
        links_created=db.dbsize() - 1 if db.exists("stats:requests") else 0,
    )


@app.post("/shorten")
def shorten():
    url = (request.get_json(silent=True) or {}).get("url", "")
    if not url.startswith(("http://", "https://")):
        return jsonify(error="send JSON like {\"url\": \"https://...\"}"), 400
    code = secrets.token_urlsafe(4)
    db.set(f"link:{code}", url)
    return jsonify(code=code, short_url=f"http://localhost:8080/{code}"), 201


@app.get("/<code>")
def follow(code):
    url = db.get(f"link:{code}")
    if url is None:
        return jsonify(error="not found"), 404
    db.incr(f"clicks:{code}")
    return redirect(url)


@app.get("/stats/<code>")
def stats(code):
    return jsonify(code=code, clicks=int(db.get(f"clicks:{code}") or 0))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
