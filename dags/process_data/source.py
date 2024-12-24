import dlt
from dlt.sources.filesystem import filesystem
from airflow.providers.amazon.aws.hooks.s3 import S3Hook
from airflow.models import Variable
from dlt.common import pendulum

def get_s3_file_list(bucket_name, prefix, s3_conn_id):
    """
    Retrieves a list of files from an S3 bucket using an Airflow S3 connection.

    Args:
        bucket_name (str): The name of the S3 bucket.
        prefix (str): The prefix (path) within the bucket to list files from.
        s3_conn_id (str): The Airflow connection ID for S3.

    Returns:
        list: A list of file keys (paths) in the S3 bucket under the given prefix.
    """
    s3_hook = S3Hook(aws_conn_id=s3_conn_id)
    keys = s3_hook.list_keys(bucket_name=bucket_name, prefix=prefix)
    return keys

def get_dlt_source(config):
    """
    Creates a dlt source based on the provided configuration.

    Args:
        config (dict): The parsed JSON configuration.

    Returns:
        dlt.source: The configured dlt source.
    """
    file_type = config["fileType"]
    source_config = config["source"]

    if file_type == "csv":
        # Use Airflow S3 connection if the path starts with 's3://'
        if source_config["path"].startswith("s3://"):
            return _configure_s3_source(source_config)
        elif source_config["path"].startswith("gs://"):
            return _configure_gcs_source(source_config)
        elif source_config["path"].startswith("https://"):
            return _configure_http_source(source_config)
        elif source_config["path"].startswith("/"):
            return _configure_local_source(source_config)
        else:
            raise ValueError(f"Unsupported source path format: {source_config['path']}")
    elif file_type == "sql":
        # Assuming you'll set up a SQL connection in Airflow
        return _configure_sql_source(source_config)
    elif file_type == "api":
        return _configure_api_source(source_config)
    else:
        raise ValueError(f"Unsupported file type: {file_type}")

def _configure_s3_source(source_config):
    """Configures a dlt source for CSV files on AWS S3."""
    s3_conn_id = Variable.get("s3_connection_id")  # Get S3 connection ID from Airflow variables
    bucket_name, prefix = source_config["path"][5:].split("/", 1) # Remove 's3://'
    file_paths = get_s3_file_list(bucket_name, prefix, s3_conn_id)
    # Adjust file paths to be full S3 URLs
    file_urls = [f"s3://{bucket_name}/{file_path}" for file_path in file_paths]

    # resource = filesystem(bucket_url=file_urls[0], credentials=dlt.secrets["s3_connection_id"])
    resource = filesystem(bucket_url=file_urls[0])
    return resource

def _configure_gcs_source(source_config):
    """Configures a dlt source for CSV files on Google Cloud Storage."""
    # Implement GCS connection using Airflow (similar to S3)
    raise NotImplementedError("Google Cloud Storage source not yet implemented.")

def _configure_http_source(source_config):
    """Configures a dlt source for CSV files accessible via HTTP/HTTPS."""
    # Implement HTTP source (you might need to handle authentication)
    raise NotImplementedError("HTTP source not yet implemented.")

def _configure_local_source(source_config):
    """Configures a dlt source for CSV files on the local filesystem."""
    # Implement local file system source
    raise NotImplementedError("Local file system source not yet implemented.")

def _configure_sql_source(source_config):
    """Configures a dlt source for a SQL database."""
    # Implement SQL source (you'll need to get connection details from Airflow)
    raise NotImplementedError("SQL source not yet implemented.")

def _configure_api_source(source_config):
    """Configures a dlt source for a REST API."""

    @dlt.resource(selected=False)
    def get_data_from_api(
        last_timestamp: dlt.sources.incremental[pendulum.DateTime] = dlt.sources.incremental(
            "timestamp", initial_value=pendulum.datetime(2023, 1, 1)
        )
    ):
        """
        Fetches data from an example API. Replace this with your actual API call.
        Implements incremental loading based on a timestamp.
        """
        api_url = source_config["url"]
        params = {"since": last_timestamp.last_value.isoformat()}
        headers = source_config.get("headers", {})  # e.g., for API keys

        response = requests.get(api_url, params=params, headers=headers)
        response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)

        data = response.json()
        for item in data:
            # Assuming the API returns a timestamp field for incremental loading
            yield item

    return get_data_from_api

def apply_column_transformations(resource, config):
    """
    Applies column transformations (like renaming or filtering) to a dlt resource.

    Args:
        resource (dlt.resource): The dlt resource to transform.
        config (dict): The parsed JSON configuration.

    Returns:
        dlt.resource: The transformed dlt resource.
    """
    columns_config = config.get("columns", [])

    # Filter columns
    selected_columns = [col["name"] for col in columns_config if col.get("isSelected", True)]
    if selected_columns:
        resource = resource.with_columns(*selected_columns)

    # Rename columns (using add_map)
    for col in columns_config:
        if "alias" in col:
            def rename_column(item, original_name=col["name"], new_name=col["alias"]):
                item[new_name] = item.pop(original_name)
                return item
            resource = resource.add_map(rename_column)

    return resource