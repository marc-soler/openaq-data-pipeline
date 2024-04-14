import mage_ai

mage_ai.run("openaq_api_to_gcs", "/home/src/mage-dbt")

mage_ai.run("openaq_gcs_to_bq", "/home/src/mage-dbt")
