from icecream import ic
import numpy as np


def analyze_fit(fit):
    ic(fit.summary())

    y_sim = fit.stan_variable("y_sim")
    n_row_total = y_sim.shape[0]
    ppd = y_sim.sum(axis=0) / n_row_total

    prob_voting = np.median(ppd)
    ic(prob_voting)

    lower_quantile, upper_quantile = (
        np.quantile(y_sim.sum(axis=0), [0.05, 0.95]) / n_row_total
    )
    ic(lower_quantile, upper_quantile)

    return (
        ppd,
        {
            "prob_voting": prob_voting,
            "lower_quantile": lower_quantile,
            "upper_quantile": upper_quantile,
        },
    )


def analyze_differences(with_bbd_ppd, without_bbd_ppd):
    difference = with_bbd_ppd - without_bbd_ppd
    p_bbd_impact = np.mean(difference > 0)
    ic(p_bbd_impact)

    return p_bbd_impact
