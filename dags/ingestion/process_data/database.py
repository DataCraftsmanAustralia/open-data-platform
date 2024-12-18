from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from typing import Dict, Any, Optional
import os

class DatabaseHandler:
    def __init__(self, connection_string: str):
        self._connection_string = connection_string
        self._engines = {}
    
    def create_engine(self, database_type: str) -> Engine:
        """Create or get a database engine for a specific type"""
        if database_type not in self._engines:
            # Modify connection string based on database type
            if database_type == 'metadata':
                conn_str = self._connection_string.replace('DATABASE', 'metadata')
            elif database_type == 'data':
                conn_str = self._connection_string.replace('DATABASE', 'data')
            elif database_type == 'log':
                conn_str = self._connection_string.replace('DATABASE', 'log')
            else:
                conn_str = self._connection_string
                
            self._engines[database_type] = create_engine(conn_str)
        return self._engines[database_type]
    
    def create_metadata_engine(self) -> Engine:
        """Create engine for metadata operations (schemas, configs)"""
        return self.create_engine('metadata')
    
    def create_data_engine(self) -> Engine:
        """Create engine for data operations"""
        return self.create_engine('data')
    
    def create_log_engine(self) -> Engine:
        """Create engine for logging operations"""
        return self.create_engine('log')
    
    def dispose_all(self):
        """Dispose all engine connections"""
        for engine in self._engines.values():
            engine.dispose()
        self._engines.clear()