
from lib import Processor
from lib.utils import load_json, get_trends_by_name
import pandas as pd
import os

# Generate trend data when endpoint is spun up.
# How do we update this trend data?
#   Just restart this end point or rerun the snippet below to generate the trend results file.

proc = Processor()
proc.load_data()
proc.preprocess()
proc.get_poly_trends()


# load trend data
trends = load_json(os.getcwd() + "/data/metadata/trends.json")
trends_df = pd.DataFrame(trends)


def predict(args):
    location_name = str(args.get('location_name'))
    result = get_trends_by_name(trends_df, location_name)

    # filter to return only color and slope
    if result:
        result = {"color": result["slope_data"]["risk"]
                  ["color"], "slope": result["slope_data"]["slope"]}
    return result

# Sample output for a valid location
# {'color': 'red', 'slope': 522.7048223423567}

# Sample output for a invalid location
# {}


# result = (get_trends_by_name(trends_df, "US-California-Santa Cldara (HQ)"))
# if result:
#     result = {"color": result["slope_data"]["risk"]
#               ["color"], "slope": result["slope_data"]["slope"]}
# print(result)
