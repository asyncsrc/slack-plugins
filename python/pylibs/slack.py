import argparse
from sys import argv


def parse_arguments():

    # cleanup quotes from cmd line args
    for index, arg in enumerate(argv):
        argv[index] = arg.replace("\"", "")

    parser = argparse.ArgumentParser()
    parser.add_argument("-team_domain")
    parser.add_argument("-channel_name")
    parser.add_argument("-user_name")
    parser.add_argument("-response_url")
    parser.add_argument("-text")
    parser.add_argument("-token")
    parser.add_argument("-team_id")
    parser.add_argument("-channel_id")
    parser.add_argument("-user_id")
    parser.add_argument("-command")

    args = parser.parse_args()
    return args


def build_app_server_list(server_letters):

    # Build our server list with fully-qualified names
    servers = []
    for server in server_letters.split(","):
        servers.append("xyz{}.xyz.com".format(server))

    return servers

