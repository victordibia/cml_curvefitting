import json


def load_json(file_path):
    with open(file_path) as f:
        data = json.load(f)
        return data


# Load trained models when model endpoint is spun up
trends = load_json("data/metadata/trends.json")


def get_predictions(location_name, end_date):
    result = [None, None, None, None]
    trend_locations = [x for x in trends if location_name in x["location"]]
    # pick first one

    if trend_locations:
        trend = trend_locations[0]
        slope_data = trend["slope_data"]
        confidence = "high" if (trend["trend_uncertainty"] < 0.1) else "low"
        print("Confidence is", confidence)
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
