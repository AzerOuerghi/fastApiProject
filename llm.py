import json
import os
import sys
from langchain_community.llms import Bedrock
import boto3
import botocore

import torch

boto3_bedrock = boto3.client(
    'bedrock-runtime',
    region_name="eu-west-2",
    aws_access_key_id='AKIA3FLD4O5D46JSNL5P',
    aws_secret_access_key="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",
)
model_id = "mistral.mixtral-8x7b-instruct-v0:1"


def boto3_invoke_model(prompt_data):
    instruction = f"<s>[INST] {prompt_data} [/INST]"
    body = {
        "prompt": instruction,
        "max_tokens": 520,
        "temperature": 0.2,
    }
    body = json.dumps(body)
    accept = 'application/json'
    contentType = 'application/json'
    try:
        response = boto3_bedrock.invoke_model(body=body, modelId=model_id, accept=accept, contentType=contentType)
        response_body = json.loads(response["body"].read())
        outputs = response_body.get("outputs")

        completions = [output["text"] for output in outputs]
        if isinstance(completions, list):
            result = completions[0]
        else:
            result = completions
        return result
    except botocore.exceptions.ClientError:
        print(f"Couldn't invoke {model_id}")


def main():
    prompt_data = "What is the capital of France?"
    result = boto3_invoke_model(prompt_data)
    print(result)


if __name__ == "__main__":
    main()
