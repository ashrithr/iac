import json
import logging
import boto3
import requests

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def handler(event, context):
    logger.info('got event {}'.format(event))
    send_response(event, context, "SUCCESS",
                  "Successfully update bucket notification policy.")
    return


def send_response(event, context, response_status, reason):
    response_body = {
        'Status': response_status,
        'Reason': "{}. For more information, Check the details in CloudWatch Log Group: {}, CloudWatch Log Stream: {}"
        .format(reason, context.log_group_name, context.log_stream_name),
        'PhysicalResourceId': event['ResourceProperties']['LambdaArn'],
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
