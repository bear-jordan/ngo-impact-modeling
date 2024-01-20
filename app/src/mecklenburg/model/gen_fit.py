from pathlib import Path

from cmdstanpy import CmdStanModel
from icecream import ic


def main():
    stan_file = Path("./mecklenburg/model/model.stan")
    model = CmdStanModel(stan_file=stan_file)
    data = {
        "N": 5,
        "alpha": [2, 3, 4, 5, 6],
        "beta": [1, 1, 1, 1, 1],
    }
    fit = model.sample(data)
    ic(fit.summary())
    n_total = fit.stan_variable("y_sim").size
    n_null_total = fit.stan_variable("y_null_sim").size
    percent_voted = fit.stan_variable("y_sim").sum() / n_total
    percent_null_voted = fit.stan_variable("y_null_sim").sum() / n_null_total

    ic(percent_voted)
    ic(percent_null_voted)


if __name__ == "__main__":
    main()
