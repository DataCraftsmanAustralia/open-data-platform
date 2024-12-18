import pandas as pd
from typing import Dict, Any, Optional
from datetime import datetime
from sqlalchemy import text
from sqlalchemy.engine import Engine

class DataWriter:
    def __init__(self, engine: Engine):
        self.engine = engine
    
    def upsert_data(self, df: pd.DataFrame, table_name: str, schema_name: str = 'public', 
                    unique_columns: list = None):
        """
        Upsert data into target table
        """
        if unique_columns is None:
            # If no unique columns specified, perform a replace
            df.to_sql(table_name, self.engine, schema=schema_name, 
                     if_exists='replace', index=False)
        else:
            # Perform upsert using unique columns
            temp_table = f"temp_{table_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            df.to_sql(temp_table, self.engine, schema=schema_name, 
                     if_exists='replace', index=False)
            
            unique_cols_str = ", ".join(unique_columns)
            update_cols = [col for col in df.columns if col not in unique_columns]
            update_stmt = ", ".join([f"{col} = EXCLUDED.{col}" for col in update_cols])
            
            upsert_query = f"""
                INSERT INTO {schema_name}.{table_name}
                SELECT * FROM {schema_name}.{temp_table}
                ON CONFLICT ({unique_cols_str})
                DO UPDATE SET {update_stmt};
                DROP TABLE {schema_name}.{temp_table};
            """
            with self.engine.begin() as conn:
                conn.execute(text(upsert_query))
    
    def log_transaction(self, config: Dict[str, Any], status: str, message: str = None):
        """
        Log transaction details to log.transactions
        """
        log_df = pd.DataFrame([{
            'config_id': config.get('config_id'),
            'status': status,
            'message': message,
            'created_at': datetime.now()
        }])
        log_df.to_sql('transactions', self.engine, schema='log', 
                      if_exists='append', index=False)
    
    def update_schedule(self, config_id: str, status: str, next_run: datetime = None):
        """
        Update schedule status in log.schedule
        """
        update_query = """
            UPDATE log.schedule
            SET status = :status,
                last_run = NOW(),
                next_run = :next_run
            WHERE config_id = :config_id
        """
        with self.engine.begin() as conn:
            conn.execute(text(update_query), 
                        {'status': status, 'next_run': next_run, 'config_id': config_id})
    
    def write_data(self, df: pd.DataFrame, config: Dict[str, Any]):
        """
        Write data to target table and log the transaction
        """
        try:
            # Get target table information from config
            target_table = config['target_table']
            target_schema = config.get('target_schema', 'public')
            unique_columns = config.get('unique_columns')
            
            # Perform the upsert
            self.upsert_data(
                df=df,
                table_name=target_table,
                schema_name=target_schema,
                unique_columns=unique_columns
            )
            
            # Log successful transaction
            self.log_transaction(
                config=config,
                status='success',
                message=f"Successfully processed {len(df)} rows"
            )
            
            # Update schedule if this is a scheduled job
            if config.get('schedule_interval'):
                self.update_schedule(
                    config_id=config['config_id'],
                    status='success'
                )
                
        except Exception as e:
            # Log failed transaction
            self.log_transaction(
                config=config,
                status='error',
                message=str(e)
            )
            
            # Update schedule if this is a scheduled job
            if config.get('schedule_interval'):
                self.update_schedule(
                    config_id=config['config_id'],
                    status='error'
                )
            
            raise e