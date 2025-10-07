from flask import Flask
import os

app = Flask(__name__)
container_name = os.getenv("APP_NAME", "Unknown")

@app.route("/")
def hello():
    return f"Hello from {container_name}"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)