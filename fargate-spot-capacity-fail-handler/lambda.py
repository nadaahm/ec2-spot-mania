import boto3
import json
import logging
import os
import time

logger = logging.getLogger('logger')
logger.setLevel(logging.INFO)

def log_error_message(e):
    logger.error(e.response['Error']['Code'])
    logger.error(e.response['Error']['Message'])
    
def lambda_handler(event, context):
    logger.debug('Event received %s ' % event)
    client = boto3.client('ecs')
    clusterName = event['resources'][0].split('/')[1]
    serviceName = event['resources'][0].split('/')[2]

    
    try:
        response = client.update_service(
        cluster = clusterName,
        service = serviceName,
        capacityProviderStrategy=[
            {
                'capacityProvider': 'FARGATE',
                'weight': 1
            },
        ],
        forceNewDeployment=True,
        )
        logger.debug('update service response %s ' % response)
    except ClientError as e:
            log_error_message(e)
    return  ("cluster: %s | service: %s | updated" %(clusterName,serviceName))
