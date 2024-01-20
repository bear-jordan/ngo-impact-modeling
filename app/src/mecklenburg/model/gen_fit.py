from pathlib import Path

from cmdstanpy import CmdStanModel
from icecream import ic


def main():
    stan_file = Path("./mecklenburg/model/model.stan")
    model = CmdStanModel(stan_file=stan_file)
    ic(model)
    ic(model.exe_info())


if __name__ == "__main__":
    main()
