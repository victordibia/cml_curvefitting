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


from lib.utils import download_file, download_taxi_csv, unzip_file, mkdir, clean_data
from tqdm import tqdm
import os
import pandas as pd

valid_years = ["2020", "2019"]
months = [str(x+1).zfill(2) for x in range(12)]
data_date_range = []  # range of data files to be downloaded from NYC Taxi
categorical_features = ["isweekday", "dayofweek", "holiday",
                        "PULocationID", "DOLocationID"]  # ["PULocationID", "DOLocationID"]
feature_list = ["passenger_count", "month", "week", "hour"]


for year in (valid_years):
    data_date_range = data_date_range + ([[year, x] for x in months])

# Create data folder
mkdir("data")
mkdir("data/zones")
mkdir("data/files")


def download_all_files(max_files=2):
    print("Downloading CSV data .. ")
    for x in tqdm(data_date_range[:max_files]):
        download_taxi_csv(x[0], x[1])

    # download shape files for plotting
    download_file(
        "https://s3.amazonaws.com/nyc-tlc/misc/taxi+_zone_lookup.csv", "data/files/zone_lookup.csv")
    download_file(
        "https://s3.amazonaws.com/nyc-tlc/misc/taxi_zones.zip", "data/files/zones_shape.zip")

    # unzip shape files
    unzip_file("data/zones_shape.zip", "data/zones")


# Build main data from samples
# Extract sample from each downloaded file and fuse into one large file

def build_from_samples(sample_size=200000):
    print("Building sampled dataset .. ")
    all_data_path = "data/all_data_df.pickle"
    train_data_ohe_path = "data/train_data_ohe_df.pickle"
    fare_labels_path = "data/fare_labels.pickle"
    triptime_labels_path = "data/triptime_labels.pickle"
    all_data_df = None

    if not os.path.isfile(all_data_path):
        df_holder = []
        for dr in tqdm(data_date_range):
            file_path = os.path.join("data/files", dr[0]+"_"+dr[1]+".csv")
            if (os.path.isfile(file_path)):
                df = pd.read_csv(file_path, parse_dates=[
                                 "tpep_pickup_datetime", "tpep_dropoff_datetime"])
                sample_size = sample_size if sample_size < df.shape[0] else df.shape[0]
                df_sample = df.copy().sample(sample_size, random_state=44)
                df_holder.append(df_sample)
        all_data_df = pd.concat(df_holder)
        all_data_df = clean_data(all_data_df, valid_years)
        all_data_df[categorical_features] = all_data_df[categorical_features].astype(
            "category")  # ensure categorical colums are categorical
        print("Sampled Dataset size:", all_data_df.shape)

        # Subset data to use only selected features
        train_data = all_data_df[feature_list + categorical_features]
        # One hot encode categorical columns
        data_ohe = pd.get_dummies(train_data[categorical_features])
        train_data_ohe = pd.concat(
            [train_data[feature_list], data_ohe], axis=1)

        # Get fare labels and trip time labels
        fare_labels = all_data_df.fare_amount
        trip_time_labels = all_data_df.trip_time

        # Save pickled version of files
        all_data_df.to_pickle(all_data_path)
        train_data_ohe.to_pickle(train_data_ohe_path)
        fare_labels.to_pickle(fare_labels_path)
        trip_time_labels.to_pickle(triptime_labels_path)

    else:
        all_data_df = pd.read_pickle(all_data_path)


download_all_files(max_files=3)
build_from_samples()
