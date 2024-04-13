from mage_ai.settings.repo import get_repo_path
from mage_ai.io.bigquery import BigQuery
from mage_ai.io.config import ConfigFileLoader
from pandas import DataFrame
import os

if "data_exporter" not in globals():
    from mage_ai.data_preparation.decorators import data_exporter


@data_exporter
def export_data_to_big_query(df: DataFrame, **kwargs) -> None:
    config_path = os.path.join(get_repo_path(), "io_config.yaml")
    config_profile = "default"
    project_id = os.environ.get("GCP_PROJECT_ID")
    dataset_id = os.environ.get("BIGQUERY_DATASET")
    table_name = os.environ.get("BIGQUERY_TABLE")
    table_id = ".".join([project_id, dataset_id, table_name])

    BigQuery.with_config(ConfigFileLoader(config_path, config_profile)).export(
        df,
        table_id,
        if_exists="replace",  # Specify resolution policy if table name already exists
    )
