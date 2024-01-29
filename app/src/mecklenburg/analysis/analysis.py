from pathlib import Path
from yaml import safe_load

from icecream import ic
import numpy as np


ANALYSIS_CFG_PATH = Path("./mecklenburg/config/analysis.yaml")


def to_str(quantile):
    return str(quantile).split(".")[-1]


def load_configurations():
    with ANALYSIS_CFG_PATH.open("r") as file:
        return safe_load(file)


def analyze_fit(fit):
    analysis_cfg = load_configurations()
    target_lower_quantile = analysis_cfg.get("lower_quantile")
    target_upper_quantile = analysis_cfg.get("upper_quantile")

    ic(fit.summary())

    y_sim = fit.stan_variable("y_sim")
    n_row_total = y_sim.shape[0]
    ppd = y_sim.sum(axis=0) / n_row_total

    prob_voting = np.median(ppd)
    ic(prob_voting)

    lower_quantile, upper_quantile = (
        np.quantile(y_sim.sum(axis=0), [target_lower_quantile, target_upper_quantile]) / n_row_total
    )
    ic(lower_quantile, upper_quantile)

    return (
        ppd,
       {
            "prob_voting": prob_voting,
            f"lower_{to_str(target_lower_quantile)}_quantile": lower_quantile,
            f"upper_{to_str(target_upper_quantile)}_quantile": upper_quantile,
        },
    )


def analyze_differences(with_ngo_ppd, without_ngo_ppd):
    difference = with_ngo_ppd - without_ngo_ppd
    p_ngo_impact = np.mean(difference > 0)
    ic(p_ngo_impact)

    return p_ngo_impact
