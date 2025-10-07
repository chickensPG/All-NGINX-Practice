from flask import Flask, render_template
import psycopg2 as pg
import os, requests, json
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__, template_folder="templates")


def get_conn():
    return pg.connect(
        dbname = os.getenv("DB_NAME"),
        user = os.getenv("DB_USER"),
        password = os.getenv("DB_PASS"),
        host = os.getenv("DB_HOST"),
        port = os.getenv("DB_PORT")
    )

def data_pop():
    conn = get_conn()
    cur = conn.cursor()
    response = requests.get("https://jsonplaceholder.typicode.com/users")
    users = response.json()
    for user in users:
        cur.execute(
            "Insert into events(user_id, event_type, event_time, metadata) values (%s, %s, now(), %s) ON CONFLICT DO NOTHING",
            (user["id"], "sign_up".lower().strip(), json.dumps({"email": user["email"]}))
        )
    conn.commit()
    cur.execute("REFRESH MATERIALIZED VIEW daily_signups;")
    conn.commit()
    cur.close()
    conn.close()


@app.get("/")
def dashboard():
    return render_template("dashboard.html")

@app.get("/api/stats/daily_signups")
def daily_signups():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("Select day, total_signups FROM daily_signups order by day;")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return [{"day": str(r[0].date()), "total_signups": r[1]} for r in rows]

if __name__ == "__main__":
    data_pop()
    app.run(host="0.0.0.0", port = 5000)
