from flask import Flask,request,jsonify
import os
from dotenv import load_dotenv
from threading import Thread
import json
import requests
import pprint
import redis

try:
    # Connect to Redis
    print("connecting to redis....")
    r = redis.Redis(host='localhost', port=6379, db=0)
    print("connected to redis")
except Exception as e:
    print("Could  not connect to redis"+e)
    exit()

queue_name = "alphaQ"

# ask from owner
load_dotenv()

repo_id=os.getenv("HARD_CODED_REPO_ID")
repo_owner=os.getenv("HARD_CODED_REPO_OWNER")
repo_default_branch=os.getenv("HARD_CODED_REPO_DEFAULT_BRANCH")

HARD_CODED_REPO_ID= int(repo_id)
HARD_CODED_REPO_OWNER=repo_owner
HARD_CODED_REPO_DEFAULT_BRANCH=f"refs/heads/{repo_default_branch}"

app = Flask(__name__)

@app.route("/",methods=["POST"])
def hello():
    data = request.json

    # print(data["repository"]["owner"]["login"])
    # print(data["repository"]["id"])
    # print(data["ref"])

    if (data["repository"]["owner"]["login"] ==HARD_CODED_REPO_OWNER and data["repository"]["id"] == HARD_CODED_REPO_ID and data["ref"]==HARD_CODED_REPO_DEFAULT_BRANCH):
        print("\nvalid push\n")
        
        all_commits_list=[]
        for item in data["commits"]:
            parsed_response = requests.get("https://api.github.com/repos/shresthjindal28/Test-repo-/commits/"+item["id"]).json()
            # This pushes all the files changes per each commit into the list
            all_commits_list.append(parsed_response["files"])

        # here we are removing unwanted entries from each files dict inside files list which is inside all_commits_list
        for commit in all_commits_list:
            for file in commit:
                file.pop("blob_url")
                file.pop("contents_url")
                file.pop("raw_url")


        data_to_send_to_agent={"commits":all_commits_list}
        print("\n\n*************commmits******************\n")
        pprint.pprint(data_to_send_to_agent)

        r.lpush(queue_name, json.dumps(data_to_send_to_agent))
        # Thread(target=agent.init_agent, args=(all_commits_list,), daemon=True).start()
        return jsonify({"status": "ok"}), 200

    else:
        print("\nnot valid push\n")
        return jsonify({"status": "ok"}), 200


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=3000, debug=True)
