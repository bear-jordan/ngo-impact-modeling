from json import dumps

from icecream import ic

from mecklenburg.data import gen_data
from mecklenburg.model import gen_fit
from mecklenburg.aws.setup import setup
from mecklenburg.aws.upload_data import upload_data
from mecklenburg.analysis import analyze_fit, analyze_differences


def fit_and_analyze(data):
    fit = gen_fit.main(data)

    return analyze_fit(fit)


def synthetic_modeling(aws_cfg, cfg):
    ic()
    # Setup Variables
    s3_client = setup()
    bucket = aws_cfg["bucket"]
    nrow = cfg["nrows"]
    p_voted_before_bbd = cfg["p_voted_before_bbd"]
    p_voted_after_bbd = cfg["p_voted_after_bbd"]

    # Create Synthetic Data
    with_bbd_raw_data, without_bbd_raw_data = gen_data.main(
        cfg, nrow, p_voted_before_bbd, p_voted_after_bbd
    )

    # Analyze Data
    with_bbd_ppd, with_bbd_results = fit_and_analyze(with_bbd_raw_data)
    without_bbd_ppd, without_bbd_results = fit_and_analyze(without_bbd_raw_data)

    # Format Results
    results = {
        "effect_size": p_voted_after_bbd - p_voted_before_bbd,
        "nrow": nrow,
        "with_bbd": with_bbd_results,
        "without_bbd": without_bbd_results,
        "p_bbd_impact": analyze_differences(with_bbd_ppd, without_bbd_ppd),
    }
    file_name = f"results/{nrow}_{p_voted_before_bbd}_{p_voted_after_bbd}.json"

    # Upload to S3 - Removed for demo
    ic(results)
    """ 
    upload_data(
        s3_client,
        dumps(results),
        bucket,
        file_name,
    )
    """
    ic("Modeling Complete")
