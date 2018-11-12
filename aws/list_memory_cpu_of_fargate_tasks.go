// To track our Fargate costs and find services which have an overly generous
// provision of CPU/memory, this script prints a list of all our active task
// definitions, along with their CPU/memory limits.
//

package main

import (
    "fmt"
    "github.com/aws/aws-sdk-go/aws/session"
    "github.com/aws/aws-sdk-go/service/ecs"
    "os"
)

func getClusterArns(client *ecs.ECS) []*string {
    var clusterArns []*string

    client.ListClustersPages(
        &ecs.ListClustersInput{},
        func(page *ecs.ListClustersOutput, _ bool) bool {
            for _, clusterArn := range page.ClusterArns {
                clusterArns = append(clusterArns, clusterArn)
            }
            return true
        })

    return clusterArns
}

func getServiceArns(client *ecs.ECS, clusterArns []*string) []*string {
    var serviceArns []*string

    for _, clusterArn := range clusterArns {
        params := &ecs.ListServicesInput {
            Cluster: clusterArn,
        }

        client.ListServicesPages(
            params,
            func(page *ecs.ListServicesOutput, _ bool) bool {
                for _, serviceArn := range page.ServiceArns {
                    serviceArns = append(serviceArns, serviceArn)
                }
                return true
            })
    }

    return serviceArns
}

func getTaskDefinitionArns(client *ecs.ECS, clusterArns []*string) []*string {
    var taskDefinitionArns []*string

    for _, clusterArn := range clusterArns {
        serviceArns := getServiceArns(client, []*string{clusterArn})

        // We have one cluster which doesn't contain any services; we should skip
        // to the next cluster.
        //
        // Note: this presents as a slightly confusing errors, as the AWS API complain
        // you didn't supply a "Services" field -- you did, but it was empty!
        //
        if len(serviceArns) == 0 {
            continue
        }

        params := &ecs.DescribeServicesInput {
            Cluster: clusterArn,
            Services: serviceArns,
        }

        describeServicesOutput, err := client.DescribeServices(params)

        if err != nil {
            fmt.Println("Error describing services: %v", err)
            os.Exit(1)
        }

        for _, service := range describeServicesOutput.Services {
            taskDefinitionArns = append(taskDefinitionArns, service.TaskDefinition)
        }
    }

    return taskDefinitionArns
}

func main() {
    sess := session.Must(session.NewSession())
    client := ecs.New(sess)

    clusterArns := getClusterArns(client)

    for _, taskDefinitionArn := range getTaskDefinitionArns(client, clusterArns) {
        params := &ecs.DescribeTaskDefinitionInput {
            TaskDefinition: taskDefinitionArn,
        }

        taskDefinitionOutput, err := client.DescribeTaskDefinition(params)

        if err != nil {
            fmt.Println("Error describing task definition %v: %v", taskDefinitionArn, err)
            os.Exit(1)
        }

        taskDefinition := taskDefinitionOutput.TaskDefinition

        // Only Fargate tasks have a top-level CPU definition.  We could drill down
        // and inspect ECS tasks as well, but as the vast majority of our ECS tasks
        // are on Fargate, I'll skip that for now.
        for _, compatibility := range taskDefinition.Compatibilities {
            if *compatibility == "FARGATE" {
                fmt.Printf("%5s\t%5s\t%s:%d\n",
                    *taskDefinition.Cpu,
                    *taskDefinition.Memory,
                    *taskDefinition.Family,
                    *taskDefinition.Revision)
                break
            }
        }
    }

    // subscriptionCountsByTopicArn := make(map[string]int)
    //
    // listTopicsParams := &sns.ListTopicsInput{}
    // listTopicsErr := snsClient.ListTopicsPages(
    //     listTopicsParams,
    //     func(page *sns.ListTopicsOutput, lastPage bool) bool {
    //         for _, topic := range page.Topics {
    //             subscriptionCountsByTopicArn[*topic.TopicArn] = 0
    //         }
    //         return true
    //     })
    //
    // if listTopicsErr != nil {
    //     fmt.Println("Error describing topics: %v", listTopicsErr)
    //     os.Exit(1)
    // }
    //
    // listSubscriptionParams := &sns.ListSubscriptionsInput{}
    // listSubscriptionsErr := snsClient.ListSubscriptionsPages(
    //     listSubscriptionParams,
    //     func(page *sns.ListSubscriptionsOutput, lastPage bool) bool {
    //         for _, subscription := range page.Subscriptions {
    //             subscriptionCountsByTopicArn[*subscription.TopicArn] += 1
    //         }
    //         return true
    //     })
    //
    // if listSubscriptionsErr != nil {
    //     fmt.Println("Error describing subscriptions: %v", listSubscriptionsErr)
    //     os.Exit(1)
    // }
    //
    // for topicArn, subscriptionCount := range subscriptionCountsByTopicArn {
    //     if subscriptionCount == 0 {
    //         fmt.Println(topicArn)
    //     }
    // }
}
