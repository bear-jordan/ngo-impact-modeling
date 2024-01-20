from pathlib import Path
from yaml import safe_load
from json import dump

from icecream import ic

from mecklenburg.data import gen_data
from mecklenburg.model import gen_fit


CFG_PATH = "./mecklenburg/config/gen-data.yaml"


def main():
    ic()
    with Path(CFG_PATH).open("r") as file:
        cfg = safe_load(file)
    params = zip(cfg["p_voted_before_bbd"], cfg["p_voted_after_bbd"])
    results = []
    for nrow in cfg["nrows"]:
        for p_voted_before_bbd, p_voted_after_bbd in params:
            gen_data.main(cfg, nrow, p_voted_before_bbd, p_voted_after_bbd)
            run_results = gen_fit.main()
            results.append({
                "effect_size": p_voted_after_bbd - p_voted_before_bbd,
                **run_results
            })

    ic(results)

    with Path("./results.json").open("w") as file:
        dump(results, file)

    ic()


if __name__ == "__main__":
    main()
