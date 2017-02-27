package slack

import (
	"bytes"
	"net/http"
	"os"

	"github.com/jessevdk/go-flags"
)

// Options -- Contains parsed commandline args
type Options struct {
	TeamDomain  string `long:"team_domain"`
	ChannelName string `long:"channel_name"`
	UserName    string `long:"user_name"`
	ResponseURL string `long:"response_url"`
	Text        string `long:"text"`
	Token       string `long:"token"`
	TeamID      string `long:"team_id"`
	ChannelID   string `long:"channel_id"`
	UserID      string `long:"user_id"`
	Command     string `long:"command"`
}

// ParseArguments returns parsed slack arguments
func ParseArguments() Options {
	options := Options{}
	flags.ParseArgs(&options, os.Args[1:])
	return options
}

// SendResponseToSlack -- Send response back to slack
func SendResponseToSlack(responseURL string, payload []byte) error {
	req, err := http.NewRequest("POST", responseURL, bytes.NewBuffer(payload))
	if err != nil {
		return err
	}

	req.Header.Set("Content-Type", "application/json")
	client := &http.Client{}
	resp, err := client.Do(req)

	if err != nil {
		return err
	}

	resp.Body.Close()

	return nil
}
