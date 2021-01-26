
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


import argparse
from flask import Flask, jsonify, request, render_template
from flask_cors import CORS, cross_origin
import logging
import os
import numpy as np
import pandas as pd
from PIL import Image
import time
import json
from lib.utils import load_json, get_trends_by_name


logging.basicConfig(level=logging.INFO)

# Point Flask to the front end directory
root_file_path = os.getcwd() + "/app"
print(root_file_path, os.getcwd())
static_folder_root = os.path.join(root_file_path, "frontend/build")
print(static_folder_root)

app = Flask(__name__, static_url_path='',
            static_folder=static_folder_root, template_folder=static_folder_root)

cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

# load locations and trend data from json
locations = load_json(os.getcwd() + "/data/metadata/locations.json")
trends = load_json(os.getcwd() + "/data/metadata/trends.json")
trends_df = pd.DataFrame(trends)


@app.route('/')
def hello():
    return render_template('index.html')


@app.route('/locations')
def get_locations():
    return jsonify(locations)


@app.route('/trends')
def get_trends():
    location_name = request.args.get('locationName')
    result = get_trends_by_name(trends_df, location_name)
    print(location_name, "locname")
    return jsonify(result)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Application parameters')
    parser.add_argument('-p', '--port', dest='port', type=int,
                        help='port to run model', default=os.environ.get("CDSW_READONLY_PORT"))

    args, unknown = parser.parse_known_args()
    port = args.port
    app.run(port=port, debug=True)
