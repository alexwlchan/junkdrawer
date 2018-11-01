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

    subscriptionCountsByTopicArn := make(map[string]int)

    listTopicsParams := &sns.ListTopicsInput{}
    listTopicsErr := snsClient.ListTopicsPages(
        listTopicsParams,
        func(page *sns.ListTopicsOutput, lastPage bool) bool {
            for _, topic := range page.Topics {
                subscriptionCountsByTopicArn[*topic.TopicArn] = 0
            }
            return true
        })

    if listTopicsErr != nil {
        fmt.Println("Error describing topics: %v", listTopicsErr)
        os.Exit(1)
    }

    listSubscriptionParams := &sns.ListSubscriptionsInput{}
    listSubscriptionsErr := snsClient.ListSubscriptionsPages(
        listSubscriptionParams,
        func(page *sns.ListSubscriptionsOutput, lastPage bool) bool {
            for _, subscription := range page.Subscriptions {
                subscriptionCountsByTopicArn[*subscription.TopicArn] += 1
            }
            return true
        })

    if listSubscriptionsErr != nil {
        fmt.Println("Error describing subscriptions: %v", listSubscriptionsErr)
        os.Exit(1)
    }

    for topicArn, subscriptionCount := range subscriptionCountsByTopicArn {
        if subscriptionCount == 0 {
            fmt.Println(topicArn)
        }
    }
}
