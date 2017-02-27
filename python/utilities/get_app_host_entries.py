#!/usr/bin/env python

import json
from pylibs import slack, saltapi
import requests

slackargs = slack.parse_arguments()

cowapi_response = requests.get("https://localhost:18080/server-ips/rackspace/xyz", verify=False)
server_map = json.loads(cowapi_response.content)

response = []

for server, ip in server_map.items():
    # format: ip address, hostname, comment with server
    response.append("{} xyz.com #{}\n".format(ip, server))
    response.append("{} api.xyz.com #{}\n\n".format(ip, server))

payload = {"text": "\n{}".format("".join(response))}

requests.post(slackargs.response_url, data=json.dumps(payload))
