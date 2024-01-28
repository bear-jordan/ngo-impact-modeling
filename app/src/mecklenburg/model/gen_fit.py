from pathlib import Path

from cmdstanpy import CmdStanModel


MODEL_PATH = Path("./mecklenburg/model/model.stan")


def process_data(raw_data):
    return {
        "N": raw_data.shape[0],
        "alpha_raw": raw_data["alpha"].values,
        "beta_raw": raw_data["beta"].values,
    }


def main(raw_data):
    stan_file = MODEL_PATH
    model = CmdStanModel(stan_file=stan_file)
    data = process_data(raw_data)

    return model.sample(data)
