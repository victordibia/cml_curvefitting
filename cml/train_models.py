import pickle
from lib.utils import load_pickle
from lib.processor import Processor
import matplotlib.pyplot as plt
import pandas as pd

models = load_pickle("data/models/fbmodels.pickle")
proc = Processor()
proc.load_data()
proc.preprocess()
proc.get_prophet_trends()
