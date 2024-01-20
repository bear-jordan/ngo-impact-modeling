from icecream import ic

from mecklenburg.data import gen_data
from mecklenburg.model import gen_fit


def main():
    ic()
    gen_data.main()
    gen_fit.main()


if __name__ == "__main__":
    main()
