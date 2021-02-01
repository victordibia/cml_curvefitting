import pickle
from lib.utils import load_json
from lib.processor import Processor
import matplotlib.pyplot as plt
import pandas as pd

location_name = "US-Maryland"
trends = load_json("data/metadata/trends.json")

result = [None, None, None, None]
trend_locations = [x for x in trends if location_name in x["location"]]
# pick first one
if trend_locations:
    trend = trend_locations[0]
    slope_data = trend["slope_data"]
    confidence = "high" if (trend["trend_uncertainty"] < 0.1) else "low"
    result = [slope_data["slope"], slope_data["risk"]
              ["label"], slope_data["risk"]["color"], confidence]
print(result)
# models = load_pickle("data/models/fbmodels.pickle")


# work_location = "US-Maryland"
# found_models = [x for x in models.keys() if work_location in x]
# model = models[found_models[0]]
# print("found models", found_models)

# end_date = "2021-12-10"
# start_date = pd.date_range(end=end_date, periods=14).tolist()[
#     0]  # start date is 14 days in past

# if model:
#     proc = Processor()

#     print(start_date)

#     forecast = proc.get_forcast(model, start_date, end_date)
#     mean_percentage_uncertainty = ((
#         (forecast.yhat_upper - forecast.yhat_lower))/2 / (forecast.yhat.abs())).mean()

#     slope_data = proc.get_slope(
#         forecast.yhat, sample_size=14)

#     confidence = "high"
#     if (mean_percentage_uncertainty > 0.1):
#         confidence = "low"

#     result = [slope_data["slope"], slope_data["risk"]
#               ["label"], slope_data["risk"]["color"], confidence]

#     print(result)

#     # print("meean error", mean_error, forecast.shape)
#     # print(slope_data)

#     # plt.plot(forecast.ds, forecast.yhat, color="orange")
#     # plt.fill_between(forecast.ds, forecast.yhat_lower,
#     #                  forecast.yhat_upper, alpha=0.2)
#     # plt.show()
