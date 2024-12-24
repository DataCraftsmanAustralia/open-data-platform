import dlt
from dlt.common.destination import Destination

def get_dlt_destination(config):
    """
    Creates a dlt destination based on the provided configuration.

    Args:
        config (dict): The parsed JSON configuration.

    Returns:
        dlt.destination: The configured dlt destination.
    """
    destination_config = config["destination"]
    destination_name = destination_config["database"]

    if destination_name == "bigquery":
        return _configure_bigquery_destination(destination_config)
    elif destination_name == "postgres":
        return _configure_postgres_destination(destination_config)
    elif destination_name == "snowflake":
        return _configure_snowflake_destination(destination_config)
    elif destination_name == "redshift":
        return _configure_redshift_destination(destination_config)
    elif destination_name == "duckdb":
        return _configure_duckdb_destination(destination_config)
    else:
        destination = Destination.from_reference(destination_name)
        return destination

def _configure_bigquery_destination(destination_config):
    """Configures a BigQuery destination."""
    # You might get credentials from Airflow variables or a service account file
    return dlt.destinations.bigquery(
        credentials=dlt.secrets.get("bigquery_credentials"),
        location=destination_config.get("location", "US")  # Default location
    )

def _configure_postgres_destination(destination_config):
    """Configures a PostgreSQL destination."""
    # Get credentials from Airflow variables
    return dlt.destinations.postgres(
        credentials=dlt.secrets.get("postgres_credentials")
    )

def _configure_snowflake_destination(destination_config):
    """Configures a Snowflake destination."""
    # Get credentials from Airflow variables
    return dlt.destinations.snowflake(
        credentials=dlt.secrets.get("snowflake_credentials")
    )

def _configure_redshift_destination(destination_config):
    """Configures a Redshift destination."""
    # Get credentials from Airflow variables
    return dlt.destinations.redshift(
        credentials=dlt.secrets.get("redshift_credentials")
    )

def _configure_duckdb_destination(destination_config):
    """Configures a DuckDB destination."""
    # DuckDB can be in-memory or file-based
    return dlt.destinations.duckdb(
        credentials=destination_config.get("credentials", ":memory:")  # Default to in-memory
    )