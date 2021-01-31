
from lib import Processor
from lib.utils import load_pickle
import pandas as pd

# Load trained models when model endpoint is spun up
models = load_pickle("data/models/fbmodels.pickle")


def get_predictions(location_name, end_date):
    # get the first model that has the given location name (two models may have same location name but diff zip codes)
    result = [None, None, None, None]
    found_models = [x for x in models.keys() if location_name in x]
    model = models[found_models[0]]

    start_date = pd.date_range(end=end_date, periods=14).tolist()[
        0]  # we will predict for last 14 days
    if model:
        proc = Processor()
        forecast = proc.get_forcast(model, start_date, end_date)
        mean_percentage_uncertainty = ((
            (forecast.yhat_upper - forecast.yhat_lower))/2 / (forecast.yhat.abs())).mean()

        slope_data = proc.get_slope(
            forecast.yhat, sample_size=14)

        # if mean_percentage_uncertainty > 10% of predicted value, we say this is low confidence.
        confidence = "high"
        if (mean_percentage_uncertainty > 0.1):
            confidence = "low"

        result = [slope_data["slope"], slope_data["risk"]
                  ["label"], slope_data["risk"]["color"], confidence]
    return result


def predict(args):
    rows = args.get("data").get("rows")
    # assumption of row[0] being location_name

    end_date = args.get('params', {}).get('updated.start')

    result = {
        "colnames": ['slope', 'risk', 'color', 'confidence'],
        "coltypes": ['REAL', 'STRING', 'STRING', 'STRING']
    }

    outRows = []
    for row in rows:

        location_name = str(row[0])
        print('location is', location_name)

        outRows.append(get_predictions(location_name, end_date))

    result['rows'] = outRows
    return {"version": "1.0", "data": result}
