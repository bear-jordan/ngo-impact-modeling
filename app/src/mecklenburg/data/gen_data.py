import pandas as pd
from numpy.random import rand, randint


def gen_person(p, max_n_elections, min_n_elections):
    n_elections = randint(low=min_n_elections, high=max_n_elections)
    did_vote = [result < p for result in rand(n_elections)]
    n_vote = sum(did_vote)
    n_no_vote = n_elections - n_vote

    return {"alpha": n_vote, "beta": n_no_vote}


def main(cfg, nrows, p_voted_before_ngo, p_voted_after_ngo):
    max_n_elections = cfg["max_n_elections"]
    min_n_elections = cfg["min_n_elections"]

    with_ngo = []
    without_ngo = []
    for _ in range(nrows):
        with_ngo.append(gen_person(p_voted_after_ngo, max_n_elections, min_n_elections))
        without_ngo.append(
            gen_person(p_voted_before_ngo, max_n_elections, min_n_elections)
        )

    return pd.DataFrame(with_ngo), pd.DataFrame(without_ngo)
