from pathlib import Path

from cmdstanpy import CmdStanModel
from icecream import ic
import numpy as np
import pandas as pd


WITH_BBD_PATH = "./with_bbd.tsv"
WITHOUT_BBD_PATH = "./without_bbd.tsv"


def load_data():
    with_bbd = pd.read_table(Path(WITH_BBD_PATH))
    without_bbd = pd.read_table(Path(WITHOUT_BBD_PATH))

    return (with_bbd, without_bbd)


def process_data(raw_data):
    return {
        "N": raw_data.shape[0],
        "alpha_raw": raw_data["alpha"].values,
        "beta_raw": raw_data["beta"].values,
    }


def analyze_data(model, data):
    fit = model.sample(data)
    ic(fit.summary())

    y_sim = fit.stan_variable("y_sim")
    n_row_total = y_sim.shape[0]
    y_sim_norm = y_sim.sum(axis=0) / n_row_total

    prob_voting = np.median(y_sim_norm)
    ic(prob_voting)

    lower_quantile, upper_quantile = np.quantile(
        y_sim.sum(axis=0), [0.05, 0.95]
    ) / n_row_total
    ic(lower_quantile, upper_quantile)

    return (
        y_sim_norm,
        {
            "prob_voting": prob_voting,
            "lower_quantile": lower_quantile,
            "upper_quantile": upper_quantile,
        }
    )


def main():
    stan_file = Path("./mecklenburg/model/model.stan")
    model = CmdStanModel(stan_file=stan_file)
    with_bbd, without_bbd = load_data()

    with_bbd_ppd, with_bbd_results = analyze_data(model, process_data(with_bbd))
    without_bbd_ppd, without_bbd_results = analyze_data(model, process_data(without_bbd))

    difference = with_bbd_ppd - without_bbd_ppd
    prob_bbd_impact = np.mean(difference > 0)
    ic(prob_bbd_impact)

    return {
        "with_bbd": with_bbd_results,
        "without_bbd": without_bbd_results,
        "prob_bbd_impact": prob_bbd_impact,
    }


if __name__ == "__main__":
    main()
