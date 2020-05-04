"""
Custom Resource Lambda for executing Step Function
"""

import json
import logging
import boto3
import requests

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def handler(event, context):
    logger.info('got event {}'.format(event))
    response_data = {}

    try:
        if event['RequestType'] == 'Create' or event['RequestType'] == 'Update':
            logger.info("Handling Create/Update request")
            if 'SF_ARN' not in event['ResourceProperties']:
                raise "Required parameters are not present"
            sf_arn = event['ResourceProperties']['SF_ARN']
            response = execute_sf(sf_arn)
            response_data = {'ExecutionArn': response}
        elif event['RequestType'] == 'Delete':
            logger.info(
                "Ignoring the DELETE request as there are no physical resources to delete")

        response_status = 'SUCCESS'
    except Exception as e:
        error_msg = "Failed to process: " + e
        logger.error(error_msg)
        response_status = 'FAILURE'
        response_data = {'Failure': error_msg}

    send_response(event, context, response_status, response_data)
    return


def execute_sf(sf_arn):
    logger.info("Triggering Step Function: %s", sf_arn)

    client = boto3.client('stepfunctions')
    try:
        response = client.start_execution(
            stateMachineArn=sf_arn,
            input='{}'
        )
        return response['executionArn']
    except Exception as e:
        logger.error("Failed triggering Step Function execution: %s", e)


def send_response(event, context, response_status, response_data, physicalResourceId=None):
    response_body = {
        'Status': response_status,
        'Reason': "{}. For more information, Check the details in CloudWatch Log Group: {}, CloudWatch Log Stream: {}"
        .format(response_data, context.log_group_name, context.log_stream_name),
        'PhysicalResourceId': physicalResourceId or context.log_stream_name,
        'StackId': event['StackId'],
        'RequestId': event['RequestId'],
        'LogicalResourceId': event['LogicalResourceId']
    }
    logger.info('RESPONSE BODY:\n %s', json.dumps(response_body))

    try:
        req = requests.put(event['ResponseURL'],
                           data=json.dumps(response_body))
        if req.status_code != 200:
            logger.error("Request object to CF is %s", req.text)
            raise Exception(
                'Received non-200 response while sending response to CloudFormation.')
        return
    except requests.exceptions.RequestException as ex:
        logger.error(
            "Exception while sending the response to CF - %s", str(ex))
        raise
