from typing import Dict, Any
from .process_data.s3 import create_storage_handler
from .process_data.schema import SchemaHandler
from .process_data.database import DatabaseHandler
from .process_data.reader import DataReader
from .process_data.writer import DataWriter
from .process_data.connections import ConnectionManager
from airflow.models import Variable

class DataProcessor:
    def __init__(self, db_conn_id: str = 'postgres_default', storage_conn_id: str = 'storage_default'):
        """
        Initialize processor with connection IDs
        
        Args:
            db_conn_id: Airflow connection ID for database
            storage_conn_id: Airflow connection ID for storage
        """
        # Get database configuration
        db_type = Variable.get('database_type', default_var='postgres')
        db_details = (ConnectionManager.get_postgres_connection(db_conn_id) 
                     if db_type == 'postgres' 
                     else ConnectionManager.get_oracle_connection(db_conn_id))
        db_conn_string = ConnectionManager.build_connection_string(db_type, db_details)
        
        # Get storage configuration
        storage_config = ConnectionManager.get_storage_connection(storage_conn_id)
        
        # Initialize handlers
        self.db_handler = DatabaseHandler(db_conn_string)
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