import os
import json
from flask import Flask, request
import requests

app = Flask(__name__)

# Authentication for user filing issue (must have read/write access to
# repository to add issue to)
notify_user = os.getenv('github_user', 'biyanisuraj')
github_token = os.getenv('github_token', '')

# Github repository in which issues should be created.
# Please make sure the repo is created within the same organisation
notify_repo = os.getenv('notify_repo', 'notify')

# Home Webhook entrypoint
@app.route('/')
def start():
    return "Welcome to Github Repository Event Notifier"

# Webhook entrypoint for Repository event Notifier
@app.route('/notify',methods=['POST'])
def notify():
    data = json.loads(request.data)

    # Fetch key attributes required for creating issue on repository events
    if ( request.headers['X-Github-Event'] == "repository"):
        action = data['action']
        repo_name = data['repository']['name']
        repo_full_name = data['repository']['full_name']
        sender = data['sender']['login']
        repo_owner = data['organization']['login']

    # Compose issue details for deleted actions
        if (action == "deleted"):
            title = "WARN : Please review - Repo {} - {} by {} "\
                        .format(repo_full_name, action, sender)
            body = ":warning:@{}, @{}: **Please review** - Repo _{}_ **{}** by @{}"\
                        .format(repo_owner,
                            notify_user,
                            repo_full_name,
                            action,
                            sender)
            assignees = [notify_user]
            labels = [action]

            response = create_github_issue(repo_owner,
                                            title,
                                            body,
                                            assignees,
                                            labels)
            if response.status_code == 201:
                return "Refer issue created at {} for repo {} {} by {} "\
                        .format(response.url, repo_full_name, action, sender)
            else:
                return "Issue creation Failed {}".format(response.content)
        else:
            return "OK - Webhook Post received for {} {} by {}"\
                        .format(action, repo_full_name, sender)
    else:
        return "OK - Webhook Post received"


# Create an issue on github.com with parameters passed
def create_github_issue(repo_owner, title, body=None, assignees=None, labels=None):
    # Url to create issues via POST
    url = 'https://api.github.com/repos/%s/%s/issues' % (repo_owner, notify_repo)

    # Set Authorization Headers using Github Token
    headers = {
        "Authorization": "token %s" % github_token,
        "Accept": "application/vnd.github.golden-comet-preview+json"
    }

    # Create issue data
    issue = {'title': title,
            'body': body,
            'assignees': assignees,
            'labels': labels }

    payload = json.dumps(issue)

    # Submit the issue to the set organisation repo
    response = requests.request("POST", url, data=payload, headers=headers)
    return response

if __name__ == '__main__':
   # Set web server Host and Port, you can override using environment variables.
   web_server_ip = os.getenv('web_server_ip', '0.0.0.0')
   web_server_port = os.getenv('web_server_port', '8080')

   # Start Webhook web server
   app.run(host=web_server_ip, port=web_server_port)
