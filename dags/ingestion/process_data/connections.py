from airflow.hooks.base import BaseHook
from typing import Dict, Any
import json

class ConnectionManager:
    @staticmethod
    def get_postgres_connection(conn_id: str = 'postgres_default') -> Dict[str, Any]:
        """Get PostgreSQL connection details"""
        conn = BaseHook.get_connection(conn_id)
        return {
            'host': conn.host,
            'port': conn.port,
            'database': conn.schema,
            'username': conn.login,
            'password': conn.password,
            'extra': json.loads(conn.extra) if conn.extra else {}
        }
    
    @staticmethod
    def get_oracle_connection(conn_id: str = 'oracle_default') -> Dict[str, Any]:
        """Get Oracle connection details"""
        conn = BaseHook.get_connection(conn_id)
        return {
            'host': conn.host,
            'port': conn.port,
            'service_name': conn.schema,
            'username': conn.login,
            'password': conn.password,
            'extra': json.loads(conn.extra) if conn.extra else {}
        }
    
    @staticmethod
    def get_smtp_connection(conn_id: str = 'smtp_default') -> Dict[str, Any]:
        """Get SMTP connection details"""
        conn = BaseHook.get_connection(conn_id)
        return {
            'host': conn.host,
            'port': conn.port,
            'username': conn.login,
            'password': conn.password,
            'extra': json.loads(conn.extra) if conn.extra else {}
        }
    
    @staticmethod
    def get_jira_connection(conn_id: str = 'jira_default') -> Dict[str, Any]:
        """Get Jira connection details"""
        conn = BaseHook.get_connection(conn_id)
        return {
            'url': conn.host,
            'username': conn.login,
            'password': conn.password,
            'extra': json.loads(conn.extra) if conn.extra else {}
        }
    
    @staticmethod
    def get_storage_connection(conn_id: str = 'storage_default') -> Dict[str, Any]:
        """Get storage (S3/MinIO) connection details"""
        conn = BaseHook.get_connection(conn_id)
        extra = json.loads(conn.extra) if conn.extra else {}
        return {
            'type': extra.get('type', 'minio'),  # minio, s3, ceph
            'endpoint_url': conn.host,
            'access_key': conn.login,
            'secret_key': conn.password,
            'region': extra.get('region'),
            'extra': extra
        }
    
    @staticmethod
    def get_http_connection(conn_id: str = 'http_default') -> Dict[str, Any]:
        """Get HTTP connection details"""
        conn = BaseHook.get_connection(conn_id)
        extra = json.loads(conn.extra) if conn.extra else {}
        return {
            'base_url': conn.host,
            'username': conn.login,
            'password': conn.password,
            'headers': extra.get('headers', {}),
            'timeout': extra.get('timeout', 30),
            'verify_ssl': extra.get('verify_ssl', True),
            'extra': extra
        }
    
    @staticmethod
    def build_connection_string(conn_type: str, details: Dict[str, Any]) -> str:
        """Build connection string from connection details"""
        if conn_type == 'postgres':
            return f"postgresql://{details['username']}:{details['password']}@{details['host']}:{details['port']}/{details['database']}"
        elif conn_type == 'oracle':
            dsn = f"(DESCRIPTION=(ADDRESS=(PROTOCOL=TCP)(HOST={details['host']})(PORT={details['port']}))(CONNECT_DATA=(SERVICE_NAME={details['service_name']})))"
            return f"oracle+cx_oracle://{details['username']}:{details['password']}@{dsn}"
        else:
            raise ValueError(f"Unsupported connection type: {conn_type}") 