from flask import Flask, request, jsonify, render_template
from pymongo import MongoClient
from datetime import datetime

app = Flask(__name__)

client = MongoClient("mongodb://localhost:27017/")
db = client["github"]
collection = db["events"]


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/webhook", methods=["POST"])
def webhook():

    data = request.json
    event = request.headers.get("X-GitHub-Event")

    if event == "push":

        author = data["pusher"]["name"]
        to_branch = data["ref"].split("/")[-1]

        record = {
            "author": author,
            "action": "push",
            "to_branch": to_branch,
            "timestamp": datetime.utcnow()
        }

        collection.insert_one(record)

    elif event == "pull_request":

        pr = data["pull_request"]

        record = {
            "author": pr["user"]["login"],
            "action": "pull_request",
            "from_branch": pr["head"]["ref"],
            "to_branch": pr["base"]["ref"],
            "timestamp": datetime.utcnow()
        }

        collection.insert_one(record)

        if pr["merged"]:

            merge_record = {
                "author": pr["merged_by"]["login"],
                "action": "merge",
                "from_branch": pr["head"]["ref"],
                "to_branch": pr["base"]["ref"],
                "timestamp": datetime.utcnow()
            }

            collection.insert_one(merge_record)

    return jsonify({"status": "ok"})


@app.route("/events")
def events():

    data = list(collection.find().sort("timestamp",-1).limit(20))

    for d in data:
        d["_id"] = str(d["_id"])

    return jsonify(data)


if __name__ == "__main__":
    app.run(debug=True,port=5000)
