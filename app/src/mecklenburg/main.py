from pathlib import Path
from yaml import safe_load

from icecream import ic

from mecklenburg.workflows.synthetic_modeling import synthetic_modeling


AWS_CFG_PATH = Path("./mecklenburg/config/aws.yaml")
CFG_PATH = Path("./mecklenburg/config/gen-data.yaml")


def load_configurations():
    with AWS_CFG_PATH.open("r") as file:
        aws_cfg = safe_load(file)
    with CFG_PATH.open("r") as file:
        cfg = safe_load(file)

    return aws_cfg, cfg


def main():
    ic()
    aws_cfg, cfg = load_configurations()
    synthetic_modeling(aws_cfg, cfg)


if __name__ == "__main__":
    main()
