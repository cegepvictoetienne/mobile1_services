import os

import pymysql
from flask import Flask, jsonify

app = Flask(__name__)


def get_connection():
    return pymysql.connect(
        host=os.environ["DB_HOST"],
        port=int(os.environ.get("DB_PORT", 3306)),
        user=os.environ["DB_USER"],
        password=os.environ["DB_PASSWORD"],
        database=os.environ["DB_NAME"],
        cursorclass=pymysql.cursors.DictCursor,
    )


@app.route("/")
def index():
    return jsonify(message="Hello from Flask!")


@app.route("/health")
def health():
    with get_connection() as conn, conn.cursor() as cur:
        cur.execute("SELECT VERSION() AS version")
        row = cur.fetchone()
    return jsonify(status="ok", mysql_version=row["version"])
