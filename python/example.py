#!/usr/bin/env python

from __future__ import print_function

from pylibs import slack, saltapi
import json
import requests

slackargs = slack.parse_arguments()
server = slackargs.text
status_code, response = saltapi.execute(server, "cmd.run", "uptime")
payload = {"text": "Received status code: {}\nResponse: {}\n".format(status_code, response)}
requests.post(slackargs.response_url, data=json.dumps(payload))
