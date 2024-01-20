from pathlib import Path

from cmdstanpy import CmdStanModel
from icecream import ic


def main():
    stan_file = Path("./mecklenburg/model/model.stan")
    model = CmdStanModel(stan_file=stan_file)
    ic(model)
    data = {
        "N": 5,
        "alpha": [2, 3, 4, 5, 6],
        "beta": [1, 1, 1, 1, 1],
    }
    fit = model.sample(data)
    ic(fit.summary())


if __name__ == "__main__":
    main()
