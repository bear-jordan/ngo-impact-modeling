from pathlib import Path
import os

import boto3
from botocore.config import Config
from dotenv import load_dotenv


DOT_ENV_PATH = Path("/code/.env")


def setup():
    if DOT_ENV_PATH.exists():
        load_dotenv(DOT_ENV_PATH)
        config = Config(
            region_name="ap-southeast-2",
            signature_version="v4",
            retries={"max_attempts": 10, "mode": "standard"},
        )

        return boto3.client(
            "s3",
            aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
            aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
            config=config,
        )
    else:
        return boto3.client("s3")
