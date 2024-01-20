from datetime import datetime
from pathlib import Path
from yaml import safe_load

from boto import client
from icecream import ic

from mecklenburg.data import gen_data
from mecklenburg.model import gen_fit


AWS_CFG_PATH = "./mecklenburg/config/aws.yaml"
CFG_PATH = "./mecklenburg/config/gen-data.yaml"


def upload_to_s3(data):
    with Path(AWS_CFG_PATH).open("r") as file:
        aws_cfg = safe_load(file)

    bucket = aws_cfg["bucket"]
    current_time = datetime.now().strftime('%Y-%m-%d-%H:%M:%S')
    name = f"results_{current_time}.json"
    s3_client = client("s3")
    s3_client.upload_file(data, bucket, name)


def main():
    ic()
    with Path(CFG_PATH).open("r") as file:
        cfg = safe_load(file)
    params = zip(cfg["p_voted_before_bbd"], cfg["p_voted_after_bbd"])
    results = []
    for nrow in cfg["nrows"]:
        for p_voted_before_bbd, p_voted_after_bbd in params:
            gen_data.main(cfg, nrow, p_voted_before_bbd, p_voted_after_bbd)
            run_results = gen_fit.main()
            results.append({
                "effect_size": p_voted_after_bbd - p_voted_before_bbd,
                **run_results
            })

    ic(results)
    upload_to_s3(results)


if __name__ == "__main__":
    main()
