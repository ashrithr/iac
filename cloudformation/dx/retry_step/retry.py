import json
import boto3
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def handler(event, context):
    logger.info(event)

    sfn = boto3.client('stepfunctions')
    sm_arn = event['state_machine_arn']

    event['retry_execution_count'] -= 1
    event = json.dumps(event)

    try:
        sfn.start_execution(stateMachineArn=sm_arn, input=event)
        logger.info("Successfully triggered state machine execution")
        return event
    except Exception as e:
        logger.error(
            "Failed triggerring state machine execution, reason: %s", e)
        return str(e)
