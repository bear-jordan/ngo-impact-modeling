from json import dumps

from icecream import ic

from mecklenburg.data import gen_data
from mecklenburg.model import gen_fit
from mecklenburg.aws.setup import setup
from mecklenburg.aws.upload_data import upload_data
from mecklenburg.analysis import analyze_fit, analyze_differences


def process_data(data):
    fit = gen_fit.main(data)

    return analyze_fit(fit)


def synthetic_modeling(aws_cfg, cfg):
    ic()
    bucket = aws_cfg["bucket"]
    s3_client = setup()
    for nrow in cfg["nrows"]:
        params = zip(cfg["p_voted_before_bbd"], cfg["p_voted_after_bbd"])
        for p_voted_before_bbd, p_voted_after_bbd in params:
            gen_data.main(cfg, nrow, p_voted_before_bbd, p_voted_after_bbd)
            with_bbd_raw_data, without_bbd_raw_data = gen_fit.load_data()
            with_bbd_ppd, with_bbd_results = process_data(with_bbd_raw_data)
            without_bbd_ppd, without_bbd_results = process_data(without_bbd_raw_data)

            results = {
                "effect_size": p_voted_after_bbd - p_voted_before_bbd,
                "nrow": nrow,
                "with_bbd": with_bbd_results,
                "without_bbd": without_bbd_results,
                "p_bbd_impact": analyze_differences(with_bbd_ppd, without_bbd_ppd),
            }
            file_name = f"results/{nrow}_{p_voted_before_bbd}_{p_voted_after_bbd}.json"
            upload_data(
                s3_client,
                dumps(results),
                bucket,
                file_name,
            )
