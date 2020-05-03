import os
import boto3
import logging
import time

logger = logging.getLogger()
logger.setLevel(logging.INFO)

runtime_region = os.environ['AWS_REGION']
dx = boto3.client('dataexchange', region=runtime_region)
s3 = boto3.client('s3')


def handler(event, context):
    dataset_id = event['dataset_id']
    bucket = event['bucket_name']

    dataset_revision = get_lastest_revision(dataset_id)
    dataset_assets = get_all_assets(dataset_id, dataset_revision.get('Id'))
    job_id = export_assets(dataset_assets, bucket)

    return {
        'message': 'Successfully executed exported job',
        'status': 'SUCCESS',
        'job_id': job_id
    }


def get_entitled_data_sets():
    data_sets = []
    result = dx.list_data_sets(Origin='ENTITLED')
    next_token = result.get('NextToken')

    data_sets += result.get('DataSets')
    while next_token:
        result = dx.list_data_sets(Origin='ENTITLED', NextToken=next_token)
        data_sets += result.get('DataSets')
        next_token = result.get('NextToken')

    return data_sets


def get_lastest_revision(dataset_id):
    result = dx.list_data_set_revisions(
        DataSetId=dataset_id,
        MaxResults=1
    )

    return result.get('Revisions')[0]


def get_all_revisions(data_set_id):

    revisions = []
    res = dx.list_data_set_revisions(DataSetId=data_set_id)
    next_token = res.get('NextToken')

    revisions += res.get('Revisions')
    while next_token:
        res = dx.list_data_set_revisions(DataSetId=data_set_id,
                                         NextToken=next_token)
        revisions += res.get('Revisions')
        next_token = res.get('NextToken')

    return revisions


def get_all_assets(data_set_id, revision_id):
    assets = []
    res = dx.list_revision_assets(DataSetId=data_set_id,
                                  RevisionId=revision_id)
    next_token = res.get('NextToken')

    assets += res.get('Assets')
    while next_token:
        res = dx.list_revision_assets(DataSetId=data_set_id,
                                      RevisionId=revision_id,
                                      NextToken=next_token)
        assets += res.get('Assets')
        next_token = res.get('NextToken')

    return assets


def export_assets(assets, bucket):
    asset_destinations = []

    for asset in assets:
        asset_destinations.append({
            "AssetId": asset.get('Id'),
            "Bucket": bucket,
            "Key": asset.get('Name')
        })

    job = dx.create_job(Type='EXPORT_ASSETS_TO_S3', Details={
        "ExportAssetsToS3": {
            "RevisionId": asset.get("RevisionId"), "DataSetId": asset.get("DataSetId"),
            "AssetDestinations": asset_destinations
        }
    })

    job_id = job.get('Id')
    dx.start_job(JobId=job_id)

    # while True:
    #     job = dx.get_job(JobId=job_id)

    #     if job.get('State') == 'COMPLETED':
    #         break
    #     elif job.get('State') == 'ERROR':
    #         raise Exception("Job {} failed to complete - {}".format(
    #             job_id, job.get('Errors')[0].get('Message'))
    #         )

    #     time.sleep(1)
    return job_id
