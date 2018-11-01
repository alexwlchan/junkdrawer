package main

import (
    "fmt"
    "github.com/aws/aws-sdk-go/aws/session"
    "github.com/aws/aws-sdk-go/service/sns"
)


func main() {
    sess := session.Must(session.NewSession())
    snsClient := sns.New(sess)

    params := &sns.ListTopicsInput{}
    var arns []string

    err := snsClient.ListTopicsPages(
        params,
        func(page *sns.ListTopicsOutput, lastPage bool) bool {
            for _, topic := range page.Topics {
                arns = append(arns, *topic.TopicArn)
            }
            return true
        })

    if err != nil {
        fmt.Println("Error describing topics: %q", err)
    } else {
        fmt.Println("ARNS = %q", arns)
        fmt.Println("Hello world!")
    }
}
