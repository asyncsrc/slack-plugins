import json
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning, SNIMissingWarning, InsecurePlatformWarning
import os

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
requests.packages.urllib3.disable_warnings(InsecurePlatformWarning)
requests.packages.urllib3.disable_warnings(SNIMissingWarning)


def execute(servers, state_module, state_module_args, pillar=""):

    slack_plugin_token = discover_api_token()

    salt_payload = {
        "state_module": state_module,
        "state_module_args": state_module_args,
        "servers": servers,
        "slack_plugin_token": slack_plugin_token,
        "pillar": pillar
    }

    try:
        salt_response = requests.post("https://localhost:18080/salt/",
                                      data=json.dumps(salt_payload),
                                      verify=False)
        salt_json_response = json.loads(salt_response.text)
    except ValueError as err:
        print("ValueError occurred during HTTP POST to salt api.  Exception: {}".format(err))
        return -1, err
    else:
        return salt_response.status_code, salt_json_response["response"]


# Ensure that the SLACK_PLUGIN_TOKEN environment variable is found
# This will store our 'secret key' that only exists on the server our plugins should be executed from

def discover_api_token():
    if "SLACK_PLUGIN_TOKEN" not in os.environ:
        print("Couldn't find expected slack plugin token environment variable.")
        exit(-1)

    return os.environ["SLACK_PLUGIN_TOKEN"]


def validate_response_code(response_url, code):
    if code != 200:
        error_code_payload = {"text": "There was an error with salt while executing the plugin."
                                      "\nStatus code: {}\nSee devops for help".format(code)}
        requests.post(response_url, data=json.dumps(error_code_payload))
        exit(-1)
