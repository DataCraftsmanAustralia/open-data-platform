from typing import Dict, Any
import json
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine

class SchemaHandler:
    def __init__(self, db_engine: Engine):
        self.engine = db_engine
    
    def get_schema(self, schema_name: str) -> Dict[str, Any]:
        """
        Retrieve JSON schema from PostgreSQL
        """
        query = """
            SELECT schema_definition 
            FROM metadata.schemas 
            WHERE schema_name = %s
        """
        with self.engine.connect() as conn:
            result = conn.execute(query, [schema_name]).fetchone()
            if result:
                return json.loads(result[0])
            raise ValueError(f"Schema {schema_name} not found") 