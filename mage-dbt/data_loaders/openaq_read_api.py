import os
import pandas as pd
import numpy as np
import requests
from requests.exceptions import RetryError
from requests.adapters import HTTPAdapter
from urllib3.util import Retry

if "data_loader" not in globals():
    from mage_ai.data_preparation.decorators import data_loader
if "test" not in globals():
    from mage_ai.data_preparation.decorators import test

API_KEY = os.environ.get("OPENAQ_API_KEY")
LOCATIONS_URL = "https://api.openaq.org/v2/locations?limit=100&page=1&offset=0&sort=desc&radius=1000&city=Madrid&order_by=lastUpdated&dump_raw=false"
PARAMETERS_URL = "https://api.openaq.org/v2/parameters?limit=100&page=1&offset=0&sort=asc&order_by=id"
START_DATE = "2019-01-01T00%3A00%3A00%2B00%3A00"
END_DATE = "2024-05-01T00%3A00%3A00%2B00%3A00"


def create_session():
    # Defining the retry strategy
    retry_strategy = Retry(
        total=4,  # Maximum number of retries
        status_forcelist=[408],  # HTTP status codes to retry on
    )
    # Create an HTTP adapter with the retry strategy and mount it to session
    adapter = HTTPAdapter(max_retries=retry_strategy)

    # Create a new session object
    session = requests.Session()
    session.mount("http://", adapter)
    session.mount("https://", adapter)

    return session


def get_locations(session):
    response_locations = session.get(
        LOCATIONS_URL,
        headers={"X-API-Key": API_KEY},
    )
    locations = response_locations.json()["results"]
    locations_list = [str(i["id"]) for i in locations]
    df_locations = pd.DataFrame(locations)

    def extract_coordinates(dictionary):
        latitude = dictionary["latitude"]
        longitude = dictionary["longitude"]
        return latitude, longitude

    df_locations[["latitude", "longitude"]] = df_locations["coordinates"].apply(
        lambda x: pd.Series(extract_coordinates(x))
    )
    df_locations_schema = {
        "location_id": np.dtype("int64"),
        "location_name": np.dtype("str"),
        "country": np.dtype("str"),
        "city": np.dtype("str"),
        "latitude": np.dtype("str"),
        "longitude": np.dtype("str"),
    }
    df_locations = df_locations.rename(
        columns={"id": "location_id", "name": "location_name"}
    )
    df_locations = df_locations.loc[:, df_locations_schema.keys()]
    df_locations = df_locations.astype(df_locations_schema)

    return df_locations, locations_list


def get_parameters(session):
    response_parameters = session.get(
        PARAMETERS_URL,
        headers={"X-API-Key": API_KEY},
    )
    parameters = response_parameters.json()["results"]
    df_parameters = pd.DataFrame(parameters)
    df_parameters_schema = {
        "parameter_id": np.dtype("int64"),
        "parameter_code": np.dtype("str"),
        "parameter_name": np.dtype("str"),
        "description": np.dtype("str"),
        "unit": np.dtype("str"),
    }
    df_parameters = df_parameters.rename(
        columns={
            "id": "parameter_id",
            "name": "parameter_code",
            "displayName": "parameter_name",
            "preferredUnit": "unit",
        }
    )
    df_parameters = df_parameters.loc[:, df_parameters_schema.keys()]
    df_parameters = df_parameters.astype(df_parameters_schema)

    return df_parameters


def get_measurements(session, locations_list):
    df_measurements = pd.DataFrame()
    df_measurements_schema = {
        "location_id": np.dtype("int64"),
        "timestamp": np.dtype("str"),
        "parameter_id": np.dtype("int64"),
        "measurement_average": np.dtype("float64"),
        "measurement_count": np.dtype("int64"),
    }
    for location in locations_list:
        page = 1
        while True:
            measurements_url = f"https://api.openaq.org/v2/averages?temporal=month&date_to={END_DATE}&date_from={START_DATE}&locations_id={location}&spatial=location&limit=1000&page={page}"
            try:
                response = session.get(
                    measurements_url,
                    headers={"X-API-Key": API_KEY},
                )
            except RetryError:
                break

            response_text = response.json()["results"]
            if len(response_text) == 0:
                break
            else:
                response_df = pd.DataFrame(response_text)
                response_df = response_df.rename(
                    columns={
                        "id": "location_id",
                        "month": "timestamp",
                        "parameterId": "parameter_id",
                        "average": "measurement_average",
                    }
                )
                response_df = response_df.loc[:, df_measurements_schema.keys()]
                response_df = response_df.astype(df_measurements_schema)
                response_df = response_df.sort_values(["timestamp", "parameter_id"])

                df_measurements = pd.concat([df_measurements, response_df])

            page += 1

    df_measurements = df_measurements.reset_index()
    df_measurements = df_measurements.rename(columns={'index': 'measurement_id'})
    df_measurements["timestamp"] = pd.to_datetime(df_measurements["timestamp"])

    return df_measurements


@data_loader
def load_data_from_api(*args, **kwargs):
    session = create_session()
    df_locations, locations_list = get_locations(session)
    df_parameters = get_parameters(session)
    df_measurements = get_measurements(session, locations_list)
    df = df_measurements.merge(df_locations, on="location_id").merge(
        df_parameters, on="parameter_id"
    )

    return df


@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, "The output is undefined"
