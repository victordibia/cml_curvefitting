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
import json
import urllib.request
import zipfile
from pandas.tseries.holiday import USFederalHolidayCalendar as calendar

import pandas as pd
import pickle


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


def save_json(file_path, data):
    with open(file_path, 'w') as f:
        json.dump(data, f)


def load_json(file_path):
    with open(file_path) as f:
        data = json.load(f)
        return data


def save_pickle(file_path, data):
    with open(file_path, 'wb') as f:
        pickle.dump(data, f, protocol=pickle.HIGHEST_PROTOCOL)


def load_pickle(file_path):
    with open(file_path, 'rb') as f:
        return pickle.load(f)


def get_trends_by_name(df, location_name):
    """Returns a dict  of trends for given location name

    Args:
        df (pd.DataFrame): [dataframe created by processor.py]
        location_name (str): [description]

    Returns:
        [dict]: dict of matched values
    """
    if (location_name):
        df = (df[df.location == location_name])
    df = df.to_dict(orient="records")
    return (df)


# df = pd.read_json("data/metadata/trends.json")
# print(get_trends_by_name(df, "US-California-Santa oi Clara (HQ)"))
