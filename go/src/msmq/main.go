package main

import (
	"log"
	"pluginlibs/src/salt"
	"pluginlibs/src/slack"
	"strings"
)

func main() {
	// N.B. It's worth mentioning that because Go doesn't do exception handling, if you want Slack to show you output for your plugin...
	// You'll need to do panic("...") or log.Fatalf("..."), which will return a non-zero exit status code.
	// Non-zero status code will be seen by slackcmdhandler, which will return plugin output (including exception, stdout, etc.) to Slack caller.
	options := slack.ParseArguments()

	// Execute returns three values:  salt status code, salt response, and error if applicable
	_, response, err := salt.Execute("prcowsa002", "cmd.run", "uptime", "")

	if err != nil {
		log.Fatalf("Failed to execute salt command.  Error: %s", err)
	}

	// Cleanup response, so it doesn't break our JSON payload
	response = strings.Replace(response, "\"", "\\\"", -1)

	var payload = []byte("{\"text\": \"Here's the uptime for our salt master at Rackspace:\n" +
		response +
		"\n... However... *please* n-o-t-e `that` I'll get the MSMQ plugin working ~soon~ before _too_ long.\"}")

	if err = slack.SendResponseToSlack(options.ResponseURL, payload); err != nil {
		log.Fatalf("Error sending response to Slack.  Reason: %s", err)
	}
}
