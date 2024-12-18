from typing import Dict, Any
from .process_data.s3 import create_storage_handler
from .process_data.schema import SchemaHandler
from .process_data.database import DatabaseHandler
from .process_data.reader import DataReader
from .process_data.writer import DataWriter

class DataProcessor:
    def __init__(self, db_connection_string: str, storage_config: Dict[str, Any]):
        """
        Initialize processor with database connection and storage configuration
        
        storage_config should contain:
        - type: 's3', 'minio', or 'ceph'
        - endpoint_url: for minio/ceph
        - access_key: storage access key
        - secret_key: storage secret key
        """
        self.db_handler = DatabaseHandler(db_connection_string)
        self.storage_handler = create_storage_handler(**storage_config)
        self.schema_handler = SchemaHandler(self.db_handler.create_metadata_engine())
        
    def process(self, config: Dict[str, Any]):
        """
        Main processing function that orchestrates the data flow
        """
        try:
            # Get data from storage
            raw_data = self.storage_handler.get_data(
                bucket=config['source']['bucket'],
                key=config['source']['key']
            )
            
            # Get schema from database
            schema = self.schema_handler.get_schema(config['schema_name'])
            
            # Parse and validate data
            reader = DataReader(schema)
            df = reader.parse_to_dataframe(raw_data)
            
            # Write data and handle logging
            writer = DataWriter(self.db_handler.create_data_engine())
            writer.write_data(df, config)
            
        except Exception as e:
            # Log error using a separate log engine
            error_writer = DataWriter(self.db_handler.create_log_engine())
            error_writer.log_transaction(config, 'error', str(e))
            raise e
    
    def get_scheduled_configs(self) -> list:
        """Get configurations for scheduled processing"""
        reader = DataReader({}, self.db_handler.create_metadata_engine())
        return reader.get_scheduled_configs()
    
    def get_stream_configs(self) -> list:
        """Get configurations for stream processing"""
        reader = DataReader({}, self.db_handler.create_metadata_engine())
        return reader.get_stream_configs()
    
    def dispose(self):
        """Clean up database connections"""
        self.db_handler.dispose_all()