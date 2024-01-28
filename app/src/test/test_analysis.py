import numpy as np
import pytest

from mecklenburg.analysis import analyze_fit, analyze_differences


class MockFit:
    def __init__(self, y_sim):
        self.y_sim = y_sim

    def stan_variable(self, var_name):
        if var_name == "y_sim":
            return self.y_sim

    def summary(self):
        return "Summary"


@pytest.fixture
def mock_fit():
    return MockFit(y_sim=np.random.rand(100, 100))


def test_analyze_fit_return(mock_fit):
    _, result = analyze_fit(mock_fit)
    assert isinstance(result, dict)
    assert "prob_voting" in result
    assert "lower_quantile" in result
    assert "upper_quantile" in result


def test_analyze_fit_quartile(mock_fit):
    _, result = analyze_fit(mock_fit)
    assert result.get("lower_quantile") < result.get("prob_voting") < result.get("upper_quantile")


def test_analyze_differences():
    n_items = 10
    with_ngo_ppd = np.ones(n_items)
    without_ngo_ppd = np.zeros(n_items)
    p_ngo_impact = analyze_differences(with_ngo_ppd, without_ngo_ppd)
    assert p_ngo_impact == 1

