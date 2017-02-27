#!/usr/bin/env python

from __future__ import print_function

import json
from pylibs import slack, saltapi
import requests
import sys

# Parse commandline arguments passed in through our SLack slash command
slackargs = slack.parse_arguments()

# Build our list of abbreviated error queues we'll use as a lookup-table
queue_mapping = {
        "aseq": "accountservice",
        "aeq": "assessment",
        "bceq": "backgroundchecks",
        "ceq": "communications",
        "cteq": "communicationstimeout",
        "caeq": "courseassignment",
        "deq": "documents",
        "eeq": "everify",
        "ieq": "integration",
        "jaseq": "jobapplicationsubmission",
        "jbaeq": "jobboardautomation",
        "mpeq": "mediaprocessing",
        "peq": "people",
        "seq": "scheduler",
        "sweq": "shraweb",
        "smseq": "sms",
        "tceq": "taxcredit"
}

# This is the executable that will flush an error queue; we just pass it an error queue name and msgId or all
nservicebus_location = r"c:\NServiceBus.2.0.0.1219\tools\returntosourcequeue.exe"

# User command input is expected to be in format:  a,b,c ieq
server_letters, error_queue = slackargs.text.split(" ")

if error_queue not in queue_mapping:
        payload = {"text": "Could not find error queue matching abbreviation: {}".format(error_queue)}
        requests.post(slackargs.response_url, data=json.dumps(payload))
        sys.exit(-1)

# Build our flushing command in format:  returntosourcequeue.exe error_queue_name all
flush_command = "{} {} {}".format(nservicebus_location,
                                  queue_mapping[error_queue] + "errorqueueproduction",
                                  "all")

# Turn our input of 'a, b, c' into xyza.xyz.com, xyzb.xyz.com, etc.
servers = ",".join(slack.build_app_server_list(server_letters))

# Send execution request to salt api and get response status code + response text
status_code, salt_response = saltapi.execute(servers, "cmd.run", flush_command)

# Send salt response back to Slack
payload = {"text": "Status code: {}\nResponse: {}\n".format(status_code, salt_response)}
requests.post(slackargs.response_url, data=json.dumps(payload))
