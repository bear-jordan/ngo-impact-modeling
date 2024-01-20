from json import dumps
from pathlib import Path
from yaml import safe_load
import os

import boto3
from botocore.exceptions import ClientError
from botocore.config import Config
from icecream import ic
from dotenv import load_dotenv

from mecklenburg.data import gen_data
from mecklenburg.model import gen_fit


AWS_CFG_PATH = Path("./mecklenburg/config/aws.yaml")
CFG_PATH = Path("./mecklenburg/config/gen-data.yaml")
DOT_ENV_PATH = Path("/code/.env")


def aws_setup():
    if DOT_ENV_PATH.exists():
        load_dotenv(DOT_ENV_PATH)
        config = Config(
            region_name='ap-southeast-2',
            signature_version='v4',
            retries={
                'max_attempts': 10,
                'mode': 'standard'
            }
        )

        return boto3.client(
            's3',
            aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
            aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
            config=config,
        )
    else:
        return boto3.client('s3')


def upload_data(s3_client, data, bucket, file_name):
    try:
        s3_client.put_object(
            Body=data,
            Bucket=bucket,
            Key=file_name,
        )
    except ClientError as e:
        raise e("Check client details")


def main():
    ic()
    with AWS_CFG_PATH.open("r") as file:
        aws_cfg = safe_load(file)
    with CFG_PATH.open("r") as file:
        cfg = safe_load(file)

    bucket = aws_cfg["bucket"]
    s3_client = aws_setup()
    for nrow in cfg["nrows"]:
        params = zip(cfg["p_voted_before_bbd"], cfg["p_voted_after_bbd"])
        for p_voted_before_bbd, p_voted_after_bbd in params:
            gen_data.main(cfg, nrow, p_voted_before_bbd, p_voted_after_bbd)
            run_results = gen_fit.main()

            results = {
                "effect_size": p_voted_after_bbd - p_voted_before_bbd,
                "nrow": nrow,
                **run_results
            }
            file_name = f"results/{nrow}_{p_voted_before_bbd}_{p_voted_after_bbd}.json"
            upload_data(
                s3_client,
                dumps(results),
                bucket,
                file_name,
            )


if __name__ == "__main__":
    main()
