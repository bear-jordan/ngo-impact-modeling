from pathlib import Path

import arviz as az
from cmdstanpy import CmdStanModel
from icecream import ic
import matplotlib.pyplot as plt


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
    idata = az.from_cmdstanpy(fit)
    az.plot_posterior(idata)
    plt.savefig("./posterior.png")


if __name__ == "__main__":
    main()
