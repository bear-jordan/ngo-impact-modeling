import numpy as np
import pandas as pd
import pytest

from mecklenburg.model.gen_fit import process_data


N = 3


@pytest.fixture
def raw_data():
    return pd.DataFrame({"alpha": np.zeros(N), "beta": np.zeros(N)})


def test_process_data_structure(raw_data):
    processed_data = process_data(raw_data)
    assert "N" in processed_data
    assert "alpha_raw" in processed_data
    assert "beta_raw" in processed_data


def test_process_data_values(raw_data):
    processed_data = process_data(raw_data)
    assert processed_data.get("N") == N
    assert all(processed_data.get("alpha_raw") == np.zeros(N))
    assert all(processed_data.get("beta_raw") == np.zeros(N))
