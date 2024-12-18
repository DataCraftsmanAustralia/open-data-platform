import pandas as pd
import json
from typing import Dict, Any, Optional
from jsonschema import validate
from sqlalchemy import text
from sqlalchemy.engine import Engine
from datetime import datetime

class DataReader:
    def __init__(self, schema: Dict[str, Any], engine: Optional[Engine] = None):
        self.schema = schema
        self.engine = engine
    
    def validate_data(self, data: str) -> Dict[str, Any]:
        """
        Validate JSON data against schema
        """
        json_data = json.loads(data)
        validate(instance=json_data, schema=self.schema)
        return json_data
    
    def parse_to_dataframe(self, data: str) -> pd.DataFrame:
        """
        Parse validated JSON data into pandas DataFrame
        """
        json_data = self.validate_data(data)
        
        # Handle both array and object inputs
        if isinstance(json_data, list):
            df = pd.json_normalize(json_data)
        else:
            df = pd.json_normalize([json_data])
        
        # Apply schema types if specified
        if 'properties' in self.schema:
            for col, prop in self.schema['properties'].items():
                if col in df.columns:
                    if prop.get('type') == 'number':
                        df[col] = pd.to_numeric(df[col])
                    elif prop.get('type') == 'integer':
                        df[col] = pd.to_numeric(df[col], downcast='integer')
                    elif prop.get('type') == 'boolean':
                        df[col] = df[col].astype(bool)
                    # Add more type conversions as needed
        
        return df
    
    def get_scheduled_configs(self) -> list:
        """Get configurations that need to be processed based on schedule"""
        if not self.engine:
            raise ValueError("Engine is required for database operations")
            
        query = """
            SELECT config 
            FROM log.schedule 
            WHERE status != 'running'
            AND next_run <= NOW()
        """
        with self.engine.connect() as conn:
            results = conn.execute(text(query)).fetchall()
            return [row[0] for row in results]
    
    def get_stream_configs(self) -> list:
        """Get configurations for stream processing"""
        if not self.engine:
            raise ValueError("Engine is required for database operations")
            
        query = """
            SELECT config 
            FROM metadata.stream_configs 
            WHERE is_active = true
        """
        with self.engine.connect() as conn:
            results = conn.execute(text(query)).fetchall()
            return [row[0] for row in results]