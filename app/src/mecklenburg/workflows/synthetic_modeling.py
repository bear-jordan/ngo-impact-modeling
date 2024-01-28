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
    p_voted_before_ngo = cfg["p_voted_before_ngo"]
    p_voted_after_ngo = cfg["p_voted_after_ngo"]

    # Create Synthetic Data
    with_ngo_raw_data, without_ngo_raw_data = gen_data.main(
        cfg, nrow, p_voted_before_ngo, p_voted_after_ngo
    )

    # Analyze Data
    with_ngo_ppd, with_ngo_results = fit_and_analyze(with_ngo_raw_data)
    without_ngo_ppd, without_ngo_results = fit_and_analyze(without_ngo_raw_data)

    # Format Results
    results = {
        "effect_size": p_voted_after_ngo - p_voted_before_ngo,
        "nrow": nrow,
        "with_ngo": with_ngo_results,
        "without_ngo": without_ngo_results,
        "p_ngo_impact": analyze_differences(with_ngo_ppd, without_ngo_ppd),
    }
    file_name = f"results/{nrow}_{p_voted_before_ngo}_{p_voted_after_ngo}.json"

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
