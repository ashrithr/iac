#!/bin/bash

#
# Computes the time it took for a DX jobs of a specified dataset to complete
#

if [[ $# -ne 1 ]]; then
    echo "Usage: $0 [dataset_id]"
    exit 1
fi

DATASET_ID=$1

aws dataexchange list-jobs \
    --data-set-id $DATASET_ID \
    --query 'Jobs[*].{Id:Id,CreatedAt:CreatedAt,UpdatedAt:UpdatedAt}' > job-results-timestamps.json

jq -c '.[]' job-results-timestamps.json | while read i; do
    created_at=$(date --date $(jq -nr "${i}|.CreatedAt") +%s)
    updated_at=$(date --date $(jq -nr "${i}|.UpdatedAt") +%s)
    job_id=$(jq -nr "${i}|.Id")

    diff=$(expr $updated_at - $created_at)
    echo "Job ${job_id} took ${diff} seconds"
done

# aws s3 ls --summarize --human-readable --recursive s3://cw-us-east-1-167270772459-ashrith/dx