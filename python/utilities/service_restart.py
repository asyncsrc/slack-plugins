#!/usr/bin/env python

from __future__ import print_function

import json
from pylibs import slack, saltapi
import requests

whitelist = ["josephgimenez", "", "", ""]

# Parse commandline arguments passed in through our slash command
slackargs = slack.parse_arguments()

if slackargs.user_name not in whitelist:
    payload = {"text": "Your user name *{}* is not in the whitelist for this command.  "
                       "\nPlease contact Vanguard".format(slackargs.user_name)}
    requests.post(slackargs.response_url, data=json.dumps(payload))
    exit(0)

service_name = slackargs.text

service_mapping = {
    'onboarding': 'prod-obi_web'
}

servers = "server1,server2"
restart_command = 'docker restart {}'.format(service_mapping[service_name])


# Send execution request to salt api and get response status code + response text
status_code, salt_response = saltapi.execute(servers, "cmd.run", restart_command)

if status_code == 200:
    payload = {"text": "Service *{}* restarted successfully".format(service_name)}
else:
    payload = {"text": "Unable to restart the service on one or more servers."
                       "  Please ask Joseph to take a look.".format(service_name)}

requests.post(slackargs.response_url, data=json.dumps(payload))
