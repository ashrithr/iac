import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def handler(event, context):
    logger.info("Executing Lambda")
    return {
        'message': 'executed lambda'
    }
