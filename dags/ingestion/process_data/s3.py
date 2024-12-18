import boto3
from typing import Any, Dict

class S3Handler:
    def __init__(self, aws_access_key_id: str = None, aws_secret_access_key: str = None):
        self.s3_client = boto3.client(
            's3',
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key
        )
    
    def get_data(self, bucket: str, key: str) -> Dict[str, Any]:
        """
        Retrieve data from S3 bucket
        """
        response = self.s3_client.get_object(Bucket=bucket, Key=key)
        return response['Body'].read().decode('utf-8') 