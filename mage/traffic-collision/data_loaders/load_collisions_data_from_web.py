import os
import requests
import sqlite3
import pandas as pd
from zipfile import ZipFile
if 'data_loader' not in globals():
    from mage_ai.data_preparation.decorators import data_loader
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test


def download(url: str, filename: str):
    with open(filename, 'wb') as f:
        with requests.get(url, stream=True) as r:
            r.raise_for_status()
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)

@data_loader
def load_data_from_web(*args, **kwargs):
    url = 'https://www.kaggle.com/datasets/alexgude/california-traffic-collision-data-from-switrs/download?datasetVersionNumber=6'
    filename = "switrs.zip"
    download(url, filename)

    print(os.path.getsize(filename))
    print(os.path.abspath(filename))
    print(os.path.isfile(filename))

    with ZipFile(os.path.abspath(filename), 'r') as zObject: 
        zObject.extractall( 
            path=".") 
    # resp = urlopen(url)
    # print(type(resp.read()))
    # myzip = ZipFile(BytesIO(resp.read()))
    # print(type(myzip))

    with sqlite3.connect("switrs.sqlite") as con:
        query = (
            "SELECT *"
            "FROM collisions "
            "WHERE latitude IS NOT NULL AND longitude IS NOT NULL"
        )

        df = pd.read_sql_query(query, con)

    return df


@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'
