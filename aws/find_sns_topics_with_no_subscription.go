package main

import (
    "fmt"
    "github.com/aws/aws-sdk-go/aws/session"
    "github.com/aws/aws-sdk-go/service/sns"
    "os"
)


func main() {
    sess := session.Must(session.NewSession())
    snsClient := sns.New(sess)

    params := &sns.ListTopicsInput{}
    subscriptionCountsByTopicArn := make(map[string]int)

    err := snsClient.ListTopicsPages(
        params,
        func(page *sns.ListTopicsOutput, lastPage bool) bool {
            for _, topic := range page.Topics {
                subscriptionCountsByTopicArn[*topic.TopicArn] = 0
            }
            return true
        })

    if err != nil {
        fmt.Println("Error describing topics: %q", err)
        os.Exit(1)
    }

    for topicArn, subscriptionCount := range subscriptionCountsByTopicArn {
        if subscriptionCount == 0 {
            fmt.Println(topicArn)
        }
    }
}
