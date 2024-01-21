from pathlib import Path

from numpy.random import rand, randint


def gen_person(p, max_n_elections, min_n_elections) -> str:
    n_elections = randint(low=min_n_elections, high=max_n_elections)
    did_vote = [result < p for result in rand(n_elections)]
    n_vote = sum(did_vote)
    n_no_vote = n_elections - n_vote

    return "\t".join([str(n_vote), str(n_no_vote)])


def main(cfg, nrows, p_voted_before_bbd, p_voted_after_bbd):
    max_n_elections = cfg["max_n_elections"]
    min_n_elections = cfg["min_n_elections"]

    with_bbd_output_path = Path(cfg["with_bbd_output_path"])
    without_bbd_output_path = Path(cfg["without_bbd_output_path"])
    headers = "alpha\tbeta\n"

    with_bbd = []
    without_bbd = []
    for _ in range(nrows):
        with_bbd.append(gen_person(p_voted_after_bbd, max_n_elections, min_n_elections))
        without_bbd.append(
            gen_person(p_voted_before_bbd, max_n_elections, min_n_elections)
        )

    with with_bbd_output_path.open("w") as file:
        file.write(headers)
        file.write("\n".join(with_bbd))

    with without_bbd_output_path.open("w") as file:
        file.write(headers)
        file.write("\n".join(without_bbd))


if __name__ == "__main__":
    main()
