from lib import Processor
import os

proc = Processor()


def test_load():
    proc.load_data()
    assert(proc.df.shape[0] > 0)


def test_preprocess():
    proc.load_data()
    proc.preprocess()
    assert(len(proc.locations) > 0 and os.path.isfile(
        "data/metadata/locations.json"))


def test_trends():
    proc.load_data()
    proc.preprocess()
    proc.get_poly_trends()
    assert(os.path.isfile("data/metadata/trends.json"))


test_trends()
