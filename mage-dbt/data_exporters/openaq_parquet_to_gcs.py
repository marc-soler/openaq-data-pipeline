from mage_ai.settings.repo import get_repo_path
from mage_ai.io.config import ConfigFileLoader
from mage_ai.io.google_cloud_storage import GoogleCloudStorage
from pandas import DataFrame
import os

if "data_exporter" not in globals():
    from mage_ai.data_preparation.decorators import data_exporter


@data_exporter
def export_data_to_google_cloud_storage(df_list: list, **kwargs) -> None:
    config_path = os.path.join(get_repo_path(), "io_config.yaml")
    config_profile = "default"
    bucket_name = os.environ.get("GCS_BUCKET")

    object_keys = ["locations.parquet", 'parameters.parquet', 'measurements.py']

    for df, object_key in zip(df_list, object_keys):
        df = DataFrame(df)
        GoogleCloudStorage.with_config(
            ConfigFileLoader(config_path, config_profile)
        ).export(
            df,
            bucket_name,
            object_key,
            format="Parquet",
        )
