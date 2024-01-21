from botocore.exceptions import ClientError


def upload_data(s3_client, data, bucket, file_name):
    try:
        s3_client.put_object(
            Body=data,
            Bucket=bucket,
            Key=file_name,
        )
    except ClientError as e:
        raise e("Check client details")
