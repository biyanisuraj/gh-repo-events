# Create Github Organisation with below repositories
- `notify`
- `deleteme`
- `delete-more`

# Setup Webhook to the notifier service
- Visit below URL to setup a new webhook
    > https://github.com/organizations/github-notify/settings/hooks/new
- Replace `<github-notify>` with your github organisation name in above URL
- Edit payload URL with your webhook service `https://<hostname>:<port>/notify`
- Change content type to `application/json`
- In the section `Which events would you like to trigger this webhook?`
    - Select option `Let me select individual events.`
    - Enable only `Respositories` check box
    - Make sure `Active` checkbox is enabled and *Add Webhook*
- If webhook service is not running you will see webhook delivery failed

# Get your github token
- Goto https://github.com/settings/profile
- Goto `Developer Settings` => `Personal Access Tokens`
- Create new token and select scope `repo -> public_repo`
- Copy the generated token and keep it safe somewhere
    > You will not be able to retrieve the same token again.

# Setup Webhook Service
- Clone the gh-repo-events repo
- Setup python virtual env named **notify**
    >`mkvirtualenv notify`
- Activate the virtual environment
    >`workon notify` or `source notify/bin/activate`
- Install requirements
    >`pip install -r requirements.txt`
- Export below variables into your environment or session
    - Set Github User related variables
        >`export github_user='<your GH username>'` **mandatory**

        >`export github_token="<your GH Access token>"` **mandatory**

    - Set repo to create issues into
        >`export notify_repo='notify'`

    - Set Webhook Webserver Host and Port
        >`export web_server_ip='0.0.0.0'`

        >`export web_server_port='8080'`

- Alternatively you can update the `.env` file with your details
    >`source .env`
- Start the web server
    >`python webhook.py`

# Test the issue creation on deleteing a repository in an organisation
- Delete repository `deleteme` in your organisation
- Check issues section under `notify` respository if new issues are created.
- Delete repository `delete-more` in your organisation
- Check if new issue is created under `notify` repository

# Troubleshooting
- Goto your organisation GH Dashboard/Home page
- Select `Settings` => `Webhooks`
- Select respective webhook for notification service
- Check `Recent Deliveries` section at the bottom of the page
- Click on the failed delivery
- Check in the response body for error message
    - Is your webhook service up and `running`
    - Is it reachable from github.com
    - Is your `access token` correct or do you see `Bad credentials` error
    - Have you created the `notify` repo or set the environment variable correctly

# Tools used to create the webhook service
- Cloud9 IDE https://c9.io
- Github Developers API documentation
- Github.com for hosting the repositories
- https://webhook.site/ to test the Webhooks and look at the payload contents
