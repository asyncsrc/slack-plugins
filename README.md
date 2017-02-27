# Slack Plugins Repository

I stripped most of the plugins out as they're specific to the company I work for.

However, these plugins are executed using the Slackcmdhandler service.

Essentially, someone sets up a slash command integration that calls the Slackcmdhandler service.
As part of the integration, the plugin we want to execute is also specified in the integration URL.

Example integration URL: https://slackcmdhandler_url:4443?plugin=customtab%2Fenable_customtab_feature.py&loader=python

Someone executes a command like: /restart_service [service_name]

The restart_service plugin is executed and passed in the service_name value, so it knows what service to reset.
