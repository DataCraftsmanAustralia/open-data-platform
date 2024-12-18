from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from typing import Dict, Any

class DatabaseHandler:
    def __init__(self, connection_string: str):
        self._connection_string = connection_string
        self._engine = None
    
    @property
    def engine(self) -> Engine:
        """Get or create SQLAlchemy engine"""
        if self._engine is None:
            self._engine = create_engine(self._connection_string)
        return self._engine
    
    def create_schema_engine(self) -> Engine:
        """Create engine for schema operations"""
        return self.engine
    
    def create_data_engine(self) -> Engine:
        """Create engine for data operations"""
        return self.engine
    
    def create_log_engine(self) -> Engine:
        """Create engine for logging operations"""
        return self.engine
    
    def dispose_all(self):
        """Dispose all engine connections"""
        if self._engine:
            self._engine.dispose()
            self._engine = None