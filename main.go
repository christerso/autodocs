package main

import (
	"github.com/Jeffail/gabs"
	"github.com/shomali11/slacker"
	"log"
	"io/ioutil"
	"fmt"
	"strings"
	"encoding/json"
	"time"
	"net/http"
)

const botKey = ""
const indexFile = ""
const docsServer = ""

func main() {
	bot := slacker.NewClient(botKey)

	bot.Command("ping", "Ping!", func(request *slacker.Request, response slacker.ResponseWriter) {
		response.Reply("pong")
	})

	bot.Command("search <word>", "Find a document.", handle)

	err := bot.Listen()
	if err != nil {
		log.Fatal(err)
	}
}

func handle(request *slacker.Request, response slacker.ResponseWriter) {
	response.Typing()

	word := request.Param("word")

	if word == "" {
		response.Reply("Usage: @zanta search blah")
		return
	}

	jsonFile, err := getIndexFile()
	if err != nil {
		fmt.Println(err)
	}

	jsonParsed, err := gabs.ParseJSON(jsonFile)
	if err != nil {
		fmt.Println(err)
	}

	results := []string{}

	children, _ := jsonParsed.S("docs").Children()
	for _, child := range children {
		doc := child.Data().(map[string]interface{})

		if strings.Contains(doc["text"].(string), word) {
			results = append(results, docsServer + doc["location"].(string))
		}
	}

	if len(results) == 0 {
		response.Reply("Nothing found :/")
	}

	b, err := json.MarshalIndent(results, "", "  ")
	if err != nil {
		fmt.Println(err)
	}

	response.Reply(strings.Trim(string(b), "[]"))
}

func getIndexFile() ([]byte, error) {
	client := http.Client{
		Timeout: time.Second * 2,
	}

	req, err := http.NewRequest(http.MethodGet, docsServer + indexFile, nil)
	if err != nil {
		return nil, err
	}

	res, getErr := client.Do(req)
	if getErr != nil {
		return nil, err
	}

	body, readErr := ioutil.ReadAll(res.Body)
	if readErr != nil {
		return nil, err
	}

	return body, nil
}
