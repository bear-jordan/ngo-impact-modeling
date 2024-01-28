import pandas as pd
import pytest

from mecklenburg.data.gen_data import gen_person, main


@pytest.fixture
def person_data():
    max_n_elections = 5
    min_n_elections = 3
    p = 0.5

    person = gen_person(p, max_n_elections, min_n_elections)

    return person, max_n_elections, min_n_elections, p


def test_gen_person_structure(person_data):
    person, max_n_elections, min_n_elections, p = person_data

    assert isinstance(person, dict)
    assert "alpha" in person
    assert "beta" in person


def test_gen_person_values(person_data):
    person, max_n_elections, min_n_elections, p = person_data

    assert (
        min_n_elections <= person.get("alpha") + person.get("beta") <= max_n_elections
    )


@pytest.fixture
def cfg():
    return {"max_n_elections": 5, "min_n_elections": 3}


@pytest.fixture
def main_data(cfg):
    n_rows = 10
    p_voted_before_ngo = 0.3
    p_voted_after_ngo = 0.7

    df_with_ngo, df_without_ngo = main(
        cfg, n_rows, p_voted_before_ngo, p_voted_after_ngo
    )

    return df_with_ngo, df_without_ngo, n_rows, p_voted_before_ngo, p_voted_after_ngo


def test_main_structure(cfg, main_data):
    (
        df_with_ngo,
        df_without_ngo,
        n_rows,
        p_voted_before_ngo,
        p_voted_after_ngo,
    ) = main_data
    assert isinstance(df_with_ngo, pd.DataFrame)
    assert isinstance(df_without_ngo, pd.DataFrame)
    assert len(df_with_ngo) == n_rows and len(df_without_ngo) == n_rows


def test_main_values(cfg, main_data):
    (
        df_with_ngo,
        df_without_ngo,
        n_rows,
        p_voted_before_ngo,
        p_voted_after_ngo,
    ) = main_data

    df_with_ngo, df_without_ngo = main(
        cfg, n_rows, p_voted_before_ngo, p_voted_after_ngo
    )

    for df in [df_with_ngo, df_without_ngo]:
        for col in ["alpha", "beta"]:
            assert all(df[col].apply(lambda x: isinstance(x, int)))
            assert all(df[col] >= 0)
