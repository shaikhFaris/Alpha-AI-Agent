from flask import Flask,request,jsonify
from threading import Thread
import agent
import requests
import pprint
import asyncio
# ask from owner
HARD_CODED_REPO_ID=1041200993
HARD_CODED_REPO_OWNER="shresthjindal28"
HARD_CODED_REPO_DEFAULT_BRANCH="refs/heads/master"

app = Flask(__name__)

@app.route("/",methods=["POST"])
def hello():
    data = request.json
    # print("🔔 Webhook received:", data)
    # pprint.pprint(data)

    print(data["repository"]["owner"]["login"])
    print(data["repository"]["id"])
    print(data["ref"])

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

        Thread(target=agent.init_agent, args=(all_commits_list,), daemon=True).start()
        return jsonify({"status": "ok"}), 200

    else:
        print("\nnot valid push\n")
        return jsonify({"status": "ok"}), 200


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=3000, debug=True)

# url = 'https://github.com/shresthjindal28/Test-repo-/compare/2c932c6c8d77...5e45b1d639e4'

# 'https://api.github.com/repos/shresthjindal28/Test-repo-/compare/718b82f970a8...0a1930f3e3ad'
# response = requests.get(url)
# print(response)
# pprint.pprint(response.content)
# print(response.json())