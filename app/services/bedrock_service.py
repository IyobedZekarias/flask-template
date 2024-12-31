"""SERVICE TO CONNECT TO AND USE BEDROCK"""
import logging
import json

import boto3


class BedrockService:
    """Client class to interact with AWS Bedrock."""

    def __init__(self, model_id, region_name='us-east-1'):
        self.model_id = model_id
        self.bedrock_client = boto3.client(
            'bedrock-runtime', region_name=region_name)

    def invoke_model(self, prompt):
        """Invokes the model with the given prompt."""
        model_kwargs = {
            "modelId": self.model_id,
            "contentType": "application/json",
            "accept": "application/json",
            "body": ""
        }

        model_kwargs["body"] = json.dumps({
            "anthropic_version": "bedrock-2023-05-31",
            "max_tokens": 1000,
            "temperature": 0,
            "top_p": 1,
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": prompt
                        }
                    ]
                }
            ]
        })

        try:
            # Invoke the model
            model_res = self.bedrock_client.invoke_model(**model_kwargs)
            response_body = model_res['body'].read().decode('utf-8')
            response_json = json.loads(response_body)
            # Extract the assistant's reply
            return response_json["content"][0]["text"]
        except Exception as exc:
            logging.exception("Error invoking model: %s", exc)
            raise
