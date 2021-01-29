# ###########################################################################
#
#  CLOUDERA APPLIED MACHINE LEARNING PROTOTYPE (AMP)
#  (C) Cloudera, Inc. 2020
#  All rights reserved.
#
#  Applicable Open Source License: Apache 2.0
#
#  NOTE: Cloudera open source products are modular software products
#  made up of hundreds of individual components, each of which was
#  individually copyrighted.  Each Cloudera open source product is a
#  collective work under U.S. Copyright Law. Your license to use the
#  collective work is as provided in your written agreement with
#  Cloudera.  Used apart from the collective work, this file is
#  licensed for your use pursuant to the open source license
#  identified above.
#
#  This code is provided to you pursuant a written agreement with
#  (i) Cloudera, Inc. or (ii) a third-party authorized to distribute
#  this code. If you do not have a written agreement with Cloudera nor
#  with an authorized and properly licensed third party, you do not
#  have any rights to access nor to use this code.
#
#  Absent a written agreement with Cloudera, Inc. (“Cloudera”) to the
#  contrary, A) CLOUDERA PROVIDES THIS CODE TO YOU WITHOUT WARRANTIES OF ANY
#  KIND; (B) CLOUDERA DISCLAIMS ANY AND ALL EXPRESS AND IMPLIED
#  WARRANTIES WITH RESPECT TO THIS CODE, INCLUDING BUT NOT LIMITED TO
#  IMPLIED WARRANTIES OF TITLE, NON-INFRINGEMENT, MERCHANTABILITY AND
#  FITNESS FOR A PARTICULAR PURPOSE; (C) CLOUDERA IS NOT LIABLE TO YOU,
#  AND WILL NOT DEFEND, INDEMNIFY, NOR HOLD YOU HARMLESS FOR ANY CLAIMS
#  ARISING FROM OR RELATED TO THE CODE; AND (D)WITH RESPECT TO YOUR EXERCISE
#  OF ANY RIGHTS GRANTED TO YOU FOR THE CODE, CLOUDERA IS NOT LIABLE FOR ANY
#  DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, PUNITIVE OR
#  CONSEQUENTIAL DAMAGES INCLUDING, BUT NOT LIMITED TO, DAMAGES
#  RELATED TO LOST REVENUE, LOST PROFITS, LOSS OF INCOME, LOSS OF
#  BUSINESS ADVANTAGE OR UNAVAILABILITY, OR LOSS OR CORRUPTION OF
#  DATA.
#
# ###########################################################################


import pandas as pd
import os
import numpy as np
import logging
from .utils import mkdir, save_json, save_pickle
import json
import fbprophet
from tqdm import tqdm

logger = logging.getLogger(__name__)


class Processor():
    def __init__(self):
        self.trends = None
        self.prophet_models = {}
        mkdir("data")
        mkdir("data/metadata")
        mkdir("data/models")

    def load_data(self, data_path="data/data.csv"):
        self.df = pd.read_csv(data_path)

    def get_color(self, val):
        if (val > 500):
            return {"color": "red", "label": "High"}
        if (val < 500 and val > 250):
            return {"color": "yellow", "label": "Medium"}
        if (val < 250):
            return {"color": "green", "label": "Low"}

    def preprocess(self, save_path="data/metadata"):

        self.df.columns = [x.split(".")[1] for x in self.df.columns]
        self.df["updated"] = pd.to_datetime(self.df['updated'])
        self.df["work_location_postal_code"] = self.df.work_location + \
            "-" + self.df.work_postal_code

        self.df.sort_values(by='updated', inplace=True, ascending=True)
        self.df["confirmed"] = self.df['confirmed'].fillna(0)

        # some metadata
        locations = (self.df.drop_duplicates(['work_location_postal_code'], keep="first")[
            ["work_location_postal_code", "geo_long", "geo_lat"]]).to_dict(orient="records")
        work_locations = (self.df[~self.df.work_location_postal_code.str.contains("-Remote")].drop_duplicates(
            ['work_location_postal_code'], keep="first")[["work_location_postal_code", "geo_long", "geo_lat"]]).to_dict(orient="records")

        self.locations = list(self.df.work_location_postal_code.unique())
        locations_dict = {"work": work_locations, "all": locations}

        save_json(os.path.join(
            save_path, "locations.json"), locations_dict)

    def get_slope(self, trend, sample_size=14):
        sample_indices = list(range(sample_size))
        if len(trend) < sample_size:
            sample_size = len(trend)
            sample_indices = list(range(len(trend)))

        # fit linear curve to last x days, get slope
        slope, intercept = np.polyfit(
            sample_indices, trend[-sample_size:], 1)
        linear_poly = np.poly1d((slope, intercept))
        slope_preds = linear_poly(sample_indices)

        # keep track of slope
        slope_data = (
            {"trend": trend[-sample_size:].tolist(),
             "slope_preds": slope_preds.tolist(), "slope": slope,
             "risk": self.get_color(slope), "intercept": intercept})
        return slope_data

    def train_forecast_model(self, df):
        p_df = pd.DataFrame(df[["updated", "confirmed"]])
        p_df.columns = ['ds', 'y']
        p_df['ds'] = pd.to_datetime(p_df['ds'])
        model = fbprophet.Prophet()
        model.fit(p_df)
        return model

    def get_forcast(self, model, start_date, end_date):
        future = pd.DataFrame(pd.date_range(
            start_date, end_date).tolist(), columns=["ds"])
        forecast = model.predict(future)
        return forecast

    def get_prophet_trends(self, locations, window_size=14, save_path="data"):
        trend_holder = []
        model_holder = {}
        for i in tqdm(range(len(locations))):
            samp = self.df[self.df.work_location_postal_code == locations[i]]

            model = self.train_forecast_model(samp)
            # keep track of model for given location
            model_holder[locations[i]] = model

            forecast = self.get_forcast(model, min(
                samp.updated), max(samp.updated))
            # ax = axes[int(i/num_cols), i%num_cols]

            # ax.plot(samp.updated, samp.confirmed, label="data")
            # ax.plot(forecast.ds, forecast.yhat.tolist(), '-k', label="trend" , color='orange')
            # ax.fill_between(forecast.ds, forecast.yhat_lower.tolist(), forecast.yhat_upper.tolist(),   alpha=0.2, label="uncertainty")

            slope_data = self.get_slope(
                forecast.yhat.tolist(), sample_size=window_size)

            trend_holder.append(
                {"data": list(samp.confirmed),
                 "location": locations[i],
                 "window_size": window_size,
                 "trend_pred": forecast.yhat.tolist(),
                 "trend_pred_upper": forecast.yhat_upper.tolist(),
                 "trend_pred_lower": forecast.yhat_lower.tolist(),
                 "slope_data": slope_data})

        self.prophet_models = model_holder
        self.trends = trend_holder
        save_json(os.path.join(
            save_path, "metadata/trends.json"), self.trends)
        save_pickle("models/fbmodel.pickle", self.prophet_models)

    def get_poly_trends(self, polynomial_degree=4, window_size=14, save_path="data/metadata"):
        trend_holder = []  # data + trend for all locs in location
        locations = self.locations
        for i in range(len(locations)):
            xdf = self.df[self.df.work_location_postal_code == locations[i]]

            # difference in days between rows
            date_diff = (xdf.updated - xdf.updated.shift(1)).dt.days
            roll_diff = date_diff.cumsum()  # cumulative sum of days
            # (np.arange(len(xdf['confirmed']))+1) # simple indices
            indices = roll_diff.replace(np.nan, 0)

            # Polynomial equation fit .. confirmed cases vs number of days since first data point.
            trend = np.polyfit(indices, xdf.confirmed, polynomial_degree)
            trendpoly = np.poly1d(trend)
            trend_pred = trendpoly(indices)  # get fitted trend results

            slope_data = self.get_slope(
                trend_pred, sample_size=window_size)

            trend_holder.append(
                {"data": list(xdf.confirmed),
                 "location": locations[i],
                 "window_size": window_size,
                 "trend_pred": trend_pred.tolist(), "slope_data": slope_data})

        self.trends = trend_holder
        save_json(os.path.join(
            save_path, "trends.json"), self.trends)
