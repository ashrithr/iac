import boto3
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

dx = boto3.client('dataexchange')


def handler(event, context):
    job_id = event['ExportDatasetResult']['job_id']

    return {
        "ExportJob": {
            "State": get_job_state(job_id)
        }
    }


def get_job_state(job_id):
    job = dx.get_job(JobId=job_id)
    logger.info(job)

    return job.get('State')  # COMPLETED or ERROR
