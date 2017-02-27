#!/usr/bin/env python

import json
from pylibs import slack, saltapi
import requests

# All commandline arguments passed to plugin from slack command handler will be accessible through slackargs
slackargs = slack.parse_arguments()

# This is the salt state we want to execute via salt api, which will launch the divot docker container
divot_state_cmd = "dockerng.divot"

# Take the list of server letters passed in as a slack argument and turn them into fully-qualified server names
servername_list = slack.build_app_server_list(slackargs.text)

# Retrieve a list of our app servers from Rackspace along with their public IP addresses
# Only our production app servers match the xyz pattern and will be returned
cowapi_response = requests.get("https://localhost:18080/server-ips/rackspace/xyz", verify=False)

# Turn the list retrieved from Rackspace into an accessible dictionary
server_map = json.loads(cowapi_response.content)

for servername in servername_list:

    # If the server letter passed in as an argument from Slack doesn't exist in the map, skip it
    # E.g., if someone accidentally enters an invalid server letter as an argument
    if servername not in server_map:
        payload = {"text": "!! Skipping *{}* since it doesn't match a server at Rackspace\n".format(servername)}
        requests.post(slackargs.response_url, data=json.dumps(payload))
        continue

    public_server_ip = server_map[servername]

    # This is the salt pillar data that we're passing to divot
    # This allows divot to know which server to hit and which server name to add to the report
    pillar = {
        "site": "prod",
        "server_ip": public_server_ip,
        "server_name": servername
    }

    # Send execution request to salt api and get response status code + response text
    # xyz is one of our docker hosts at Rackspace
    # Credentials used by divot along with browser, tests to run, etc., are stored in part as a salt state
    status_code, salt_response = saltapi.execute("docker_host",
                                                 "state.sls",
                                                 divot_state_cmd,
                                                 json.dumps(pillar))

    # TODO: Parse JSON response and provide quick report to Slack

    # Send salt response back to Slack about current iteration
    payload = {"text": "Status code: {}\nSalt command: {}\nResponse{}\n".format(status_code,
                                                                                divot_state_cmd,
                                                                                salt_response)}
    requests.post(slackargs.response_url, data=json.dumps(payload))

# Send final response back to Slack
payload = {"text": "\nFinished running divot against servers: {}\n".format(servername_list)}
requests.post(slackargs.response_url, data=json.dumps(payload))
