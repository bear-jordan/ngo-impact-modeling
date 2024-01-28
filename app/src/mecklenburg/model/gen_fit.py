from pathlib import Path

from cmdstanpy import CmdStanModel
from icecream import ic
import numpy as np
import pandas as pd


def process_data(raw_data):
    return {
        "N": raw_data.shape[0],
        "alpha_raw": raw_data["alpha"].values,
        "beta_raw": raw_data["beta"].values,
    }


def main(raw_data):
    stan_file = Path("./mecklenburg/model/model.stan")
    model = CmdStanModel(stan_file=stan_file)
    data = process_data(raw_data)

    return model.sample(data)


if __name__ == "__main__":
    main()
