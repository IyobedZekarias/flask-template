"""SERVICE FOR CONNECTING TO AND USING DYNAMODB"""
import logging
import boto3
from boto3.dynamodb.types import TypeDeserializer, TypeSerializer
from flask import current_app

from app.utils.exceptions import APPError

logger = logging.getLogger(__name__)


class DynamoService:
    """
    Client class to interact with AWS Dynamo DB.
    """

    def __init__(self, table_name):

        self.dynamo_client = boto3.client(
            'dynamodb', current_app.config.get('AWS_REGION', 'us-east-1'))
        dynamo_resource = boto3.resource(
            'dynamodb', region_name=current_app.config.get('AWS_REGION', 'us-east-1'))
        self.table = dynamo_resource.Table(current_app.config.get(table_name))
        self.table_name = current_app.config.get(table_name)

    def dynamo_obj_to_python_obj(self, dynamo_obj: dict) -> dict:
        """converts a return of dynamo to a valid python dictionary"""
        deserializer = TypeDeserializer()
        return {
            k: deserializer.deserialize(v)
            for k, v in dynamo_obj.items()
        }

    def python_obj_to_dynamo_obj(self, python_obj: dict) -> dict:
        """converts a valid python dictionary to a structure that dynamo db would expect"""
        serializer = TypeSerializer()
        return {
            k: serializer.serialize(v)
            for k, v in python_obj.items()
        }

    def create(self, item: dict):
        """creates a document in dynamo db"""
        try:
            self.table.put_item(Item=item)
        except Exception as exc:
            logger.error("%s", exc)
            raise APPError(
                f'unable to put item in table {self.table_name}') from exc

    def read(self, **kwargs):
        """reads from dynamo db, accepts kwargs to fit the query function from dynamo"""
        try:
            response = self.dynamo_client.query(
                TableName=self.table_name,
                **kwargs
            )
        except Exception as exc:
            logger.error("%s", exc)
            raise APPError(
                f'unable to read from table {self.table_name}') from exc
        return response

    def update(self, **kwargs):
        """updates an item in dynamo db accepts kwargs to fit the update_item function from dynamo"""
        try:
            response = self.dynamo_client.update_item(
                TableName=self.table_name,
                **kwargs
            )
        except Exception as exc:
            logger.error("%s", exc)
            raise APPError(
                f'unable to update table {self.table_name}') from exc
        return response

    def delete(self, **kwargs):
        """deletes an item in dynamo db accepts kwargs to fit the delete_item function from dynamo"""
        try:
            response = self.dynamo_client.delete_item(
                TableName=self.table_name,
                **kwargs
            )
        except Exception as exc:
            logger.error("%s", exc)
            raise APPError(
                f'unable to update table {self.table_name}') from exc
        return response
