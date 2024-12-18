from typing import Dict, Any
from .process_data.s3 import S3Handler
from .process_data.schema import SchemaHandler
from .process_data.database import DatabaseHandler
from .process_data.reader import DataReader
from .process_data.writer import DataWriter

class DataProcessor:
    def __init__(self, db_connection_string: str, aws_access_key_id: str = None, 
                 aws_secret_access_key: str = None):
        self.db_handler = DatabaseHandler(db_connection_string)
        self.s3_handler = S3Handler(aws_access_key_id, aws_secret_access_key)
        self.schema_handler = SchemaHandler(self.db_handler.engine)
        
    def process(self, config: Dict[str, Any]):
        """
        Main processing function that orchestrates the data flow
        """
        # Get data from S3
        raw_data = self.s3_handler.get_data(
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
    
    def get_scheduled_configs(self) -> list:
        """Get configurations for scheduled processing"""
        reader = DataReader({}, self.db_handler.create_log_engine())
        return reader.get_scheduled_configs()
    
    def get_stream_configs(self) -> list:
        """Get configurations for stream processing"""
        reader = DataReader({}, self.db_handler.create_log_engine())
        return reader.get_stream_configs()
    
    def dispose(self):
        """Clean up database connections"""
        self.db_handler.dispose_all()