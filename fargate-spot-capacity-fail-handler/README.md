# Fargate Spot insufficient capacity event handler
Customers use AWS Fargate Spot to run interruption tolerant workloads. Fargate Spot uses spare capacity to run tasks, sometimes customers need to have a mechanism to take an action when spare capacity is not available.

This solution provides that mechanism to take an action when Fargate Spot fails to launch tasks due to lack of spare capacity. The solution deploys an EventBridge rule  to listen for task placement failure event and a lambda function to update the ECS service to run 100% on Fargate.

## Deploy stack

```bash
aws cloudformation create-stack --stack-name fargate-spot-capacity-fail-handler --template-body file://template.yaml --capabilities CAPABILITY_IAM
```

## Test
* Create ECS service with Fargate Spot as the capacity provider
* Set Fargate 'Platform version' to 1.4.0
* At the time of creating this solution, Fargate Spot didn't have capacity with Platform version 1.4 which will trigger Task Placement Failure Event.
* Lambda function should be triggered and switch the service to run 100% on Fargate.

## Delete stack

```bash
aws cloudformation delete-stack --stack-name fargate-spot-capacity-fail-handler
```

## Details

Example Service Task Placement Failure Event

Service task placement failure events are delivered in the following format. For more information about EventBridge parameters, see Events and Event Patterns in the Amazon EventBridge User Guide.

In the following example, the task was attempting to use the FARGATE_SPOT capacity provider but the service scheduler was unable to acquire any Fargate Spot capacity.

```json
{
    "version": "0",
    "id": "ddca6449-b258-46c0-8653-e0e3a6d0468b",
    "detail-type": "ECS Service Action",
    "source": "aws.ecs",
    "account": "111122223333",
    "time": "2019-11-19T19:55:38Z",
    "region": "us-west-2",
    "resources": [
        "arn:aws:ecs:us-west-2:111122223333:service/default/servicetest"
    ],
    "detail": {
        "eventType": "ERROR",
        "eventName": "SERVICE_TASK_PLACEMENT_FAILURE",
        "clusterArn": "arn:aws:ecs:us-west-2:111122223333:cluster/default",
        "capacityProviderArns": [
            "arn:aws:ecs:us-west-2:111122223333:capacity-provider/FARGATE_SPOT"
        ],
        "reason": "RESOURCE:FARGATE",
        "createdAt": "2019-11-06T19:09:33.087Z"
    }
}
```

## Event Pattern

```json
{
  "source": [
    "aws.ecs"
  ],
  "detail-type": [
   "ECS Service Action"
  ],
  "detail": {
  "eventName": ["SERVICE_TASK_PLACEMENT_FAILURE"]
 }
}
```
