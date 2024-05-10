import redis
import boto3
import json
import cachetools.func

from typing import Union, Tuple


class SecretsManagerProvider(redis.CredentialProvider):
    def __init__(self, secret_id, version_id=None, version_stage='AWSCURRENT'):
        self.ssm_client = boto3.client('ssm')
        self.secret_id = secret_id
        self.version_id = version_id
        self.version_stage = version_stage

    def get_credentials(self) -> Union[Tuple[str], Tuple[str, str]]:
        @cachetools.func.ttl_cache(maxsize=128, ttl=24 * 60 * 60) #24h
        def get_sm_user_credentials(secret_id, version_id, version_stage):
            secret = self.ssm_client.get_parameter(Name=secret_id, WithDecryption=True)
            secret_value = secret['Parameter']['Value']
            return json.loads(secret_value)
        creds = get_sm_user_credentials(self.secret_id, self.version_id, self.version_stage)
        return creds['username'], creds['password']