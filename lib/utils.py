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


import os
import urllib.request
import zipfile
from pandas.tseries.holiday import USFederalHolidayCalendar as calendar


def mkdir(dir_path):
    os.makedirs(dir_path, exist_ok=True)


def download_file(url, file_path):
    try:
        urllib.request.urlretrieve(url, file_path)
    except Exception as e:
        print("Unable to download file", str(e), url)


def unzip_file(zip_file_path, zip_file_destination):
    if os.path.isfile(zip_file_path):
        with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
            zip_ref.extractall(zip_file_destination)
    else:
        print("Zip file does not exist.", zip_file_path)


def download_taxi_csv(year, month, s3_source="https://s3.amazonaws.com/nyc-tlc/trip+data/yellow_tripdata_"):
    file_url = s3_source + str(year) + "-" + str(month) + ".csv"
    file_path = "data/files/" + str(year) + "_" + str(month) + ".csv"
    if not os.path.isfile(file_path):
        download_file(file_url, file_path)


def clean_data(df, valid_years):
    cal = calendar()
    df["pickup_date_only"] = df['tpep_pickup_datetime'].dt.normalize()
    df["dropoff_date_only"] = df['tpep_dropoff_datetime'].dt.normalize()
    holidays = cal.holidays(
        start=df.pickup_date_only.min(), end=df.pickup_date_only.max())
    df['holiday'] = (df['pickup_date_only'].isin(holidays)).astype(int)

    df["trip_time"] = (df.tpep_dropoff_datetime -
                       df.tpep_pickup_datetime).dt.total_seconds() / 60
    df["month"] = df.tpep_pickup_datetime.dt.month
    df["week"] = df.tpep_pickup_datetime.dt.isocalendar().week
    df["dayofweek"] = df.tpep_pickup_datetime.dt.dayofweek
    df["isweekday"] = (
        (df.tpep_pickup_datetime.dt.dayofweek) // 5 == 1).astype(float)
    df["hour"] = df.tpep_pickup_datetime.dt.hour
    df["year"] = df.tpep_pickup_datetime.dt.year
    df = df[df.trip_time >= 0]  # drop rows with negative trip times
    df = df[df.trip_distance >= 0]  # drop rows with negative trip distance
    df = df[df.fare_amount >= 0]  # drop rows with negative fare
    df = df.dropna(how='any', axis='rows')

    df = df[df.trip_distance < 100]
    df = df[df.trip_time < 100]
    df = df[df.tolls_amount < 100]
    df = df[df.fare_amount < 100]
    df = df[df.mta_tax < 30]

    # remove any years outside current consideration
    df = df[df.year.isin(valid_years)]
    df = df[df.passenger_count > 0]  # remove trips with 0 or less passengers!

    return df
