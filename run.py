import pandas as pd
from pymongo import MongoClient
from sklearn.cluster import KMeans

def _connect_mongo(host, port, username, password, db):
    """ A util for making a connection to mongo """

    if username and password:
        mongo_uri = 'mongodb+srv://%s:%s@%s/%s?retryWrites=true&w=majority' % (username, password, host, db)
        conn = MongoClient(mongo_uri)
    else:
        conn = MongoClient(host, port)
    return conn[db]


def read_mongo(db, collection, query={}, host='localhost', port=27017, username=None, password=None, no_id=True):
    """ Read from Mongo and Store into DataFrame """

    # Connect to MongoDB
    db = _connect_mongo(host=host, port=port, username=username, password=password, db=db)

    # Make a query to the specific DB and Collection
    cursor = db[collection].find(query)

    # Expand the cursor and construct the DataFrame
    df =  pd.DataFrame(list(cursor))

    # Delete the _id
    if no_id:
        del df['_id']

    return df

DB = "UnderArmour"
COLLECTION = "routes"
QUERY = {}
HOST = "underarmour.ef9ge.mongodb.net"
PORT = 27017
USERNAME = "kiulam"
PASSWORD = "kiulam"
NO_ID = True

df = read_mongo(DB, COLLECTION, QUERY, HOST, PORT, USERNAME, PASSWORD, NO_ID)
X = df[["distance"]]

kmeans = KMeans(n_clusters=3, random_state=0).fit(X)
print(kmeans.cluster_centers_)


"""
name: Python Package using Conda

on: [push]

jobs:
  build-linux:
    runs-on: ubuntu-latest
    strategy:
      max-parallel: 5

    steps:
    - uses: actions/checkout@v2
    - name: Set up Python 3.8
      uses: actions/setup-python@v2
      with:
        python-version: 3.8
    - name: Install dependencies
      run: |
        # $CONDA is an environment variable pointing to the root of the miniconda directory
        $CONDA/bin/conda env update --file environment.yml --name dev
    - name: Check Conda dependencies
      run: |
        # to see all packages installed in the active conda environment 
        conda list
#     - name: Lint with flake8
#       run: |
#         $CONDA/bin/conda install flake8
#         # stop the build if there are Python syntax errors or undefined names
#         $CONDA/bin/flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
#         # exit-zero treats all errors as warnings. The GitHub editor is 127 chars wide
#         $CONDA/bin/flake8 . --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics
#     - name: Test with pytest
#       run: |
#         conda install pytest
#         $CONDA/bin/pytest

"""