import boto3
from typing import Dict, Any, Optional
import os
from abc import ABC, abstractmethod

class ObjectStorageHandler(ABC):
    @abstractmethod
    def get_data(self, bucket: str, key: str) -> str:
        """Retrieve data from object storage"""
        pass

class S3Handler(ObjectStorageHandler):
    def __init__(self, aws_access_key_id: str = None, aws_secret_access_key: str = None):
        self.s3_client = boto3.client(
            's3',
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key
        )
    
    def get_data(self, bucket: str, key: str) -> str:
        """Retrieve data from S3 bucket"""
        response = self.s3_client.get_object(Bucket=bucket, Key=key)
        return response['Body'].read().decode('utf-8')

class MinIOHandler(ObjectStorageHandler):
    def __init__(self, endpoint_url: str, access_key: str = None, secret_key: str = None):
        self.s3_client = boto3.client(
            's3',
            endpoint_url=endpoint_url,
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_key
        )
    
    def get_data(self, bucket: str, key: str) -> str:
        """Retrieve data from MinIO bucket"""
        response = self.s3_client.get_object(Bucket=bucket, Key=key)
        return response['Body'].read().decode('utf-8')

class CephHandler(ObjectStorageHandler):
    def __init__(self, endpoint_url: str, access_key: str = None, secret_key: str = None):
        self.s3_client = boto3.client(
            's3',
            endpoint_url=endpoint_url,
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_key
        )
    
    def get_data(self, bucket: str, key: str) -> str:
        """Retrieve data from Ceph bucket"""
        response = self.s3_client.get_object(Bucket=bucket, Key=key)
        return response['Body'].read().decode('utf-8')

def create_storage_handler(storage_type: str, **kwargs) -> ObjectStorageHandler:
    """Factory function to create appropriate storage handler"""
    handlers = {
        's3': S3Handler,
        'minio': MinIOHandler,
        'ceph': CephHandler
    }
    
    if storage_type not in handlers:
        raise ValueError(f"Unsupported storage type: {storage_type}")
        
    return handlers[storage_type](**kwargs)