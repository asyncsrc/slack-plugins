package salt

import (
	"bytes"
	"crypto/tls"
	"encoding/json"
	"fmt"
	"io/ioutil"
	"net/http"
	"os"
)

// Execute SaltAPI request
func Execute(servers, stateModule, stateModuleArgs, pillar string) (int, string, error) {
	var parsedResponseBody map[string]interface{}

	slackPluginToken, err := discoverAPIToken()
	if err != nil {
		return 0, "", err
	}

	saltExecutionDetails := map[string]string{
		"state_module":       stateModule,
		"state_module_args":  stateModuleArgs,
		"servers":            servers,
		"slack_plugin_token": slackPluginToken,
		"pillar":             pillar,
	}

	payload, _ := json.Marshal(saltExecutionDetails)
	req, err := http.NewRequest("POST", "https://localhost:18080/salt/", bytes.NewBuffer(payload))

	// http://stackoverflow.com/questions/12122159/golang-how-to-do-a-https-request-with-bad-certificate
	transport := &http.Transport{
		TLSClientConfig: &tls.Config{InsecureSkipVerify: true},
	}
	client := &http.Client{Transport: transport}

	resp, err := client.Do(req)
	if err != nil {
		return 0, "", err
	}
	defer resp.Body.Close()

	responseBody, _ := ioutil.ReadAll(resp.Body)
	if err := json.Unmarshal(responseBody, &parsedResponseBody); err != nil {
		return 0, "", err
	}

	saltResponse, _ := parsedResponseBody["response"].(string)
	return resp.StatusCode, saltResponse, nil
}

func discoverAPIToken() (string, error) {
	if slackPluginToken := os.Getenv("SLACK_PLUGIN_TOKEN"); slackPluginToken != "" {
		return slackPluginToken, nil
	}
	error := fmt.Errorf("Unable to find slack plugin token in environment variable.\nAborting.")
	return "", error
}
