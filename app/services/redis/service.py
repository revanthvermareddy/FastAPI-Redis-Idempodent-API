import redis
from loguru import logger

from app.services.redis.credential_providers.ssm import SecretsManagerProvider
from app.settings import redis_settings


class RedisConnector:
    def __init__(self, host: str, port: int, credential_provider, decode_responses=True):
        self.host = host
        self.port = port
        self.credential_provider = credential_provider
        self.decode_responses = decode_responses
        self.redis_client = None

    def connect(self):
        self.redis_client = redis.Redis(host=self.host, port=self.port, credential_provider=self.credential_provider, decode_responses=self.decode_responses)
        self.redis_client.ping()
        logger.info("Connected to Redis")

    def disconnect(self):
        self.redis_client.close()
        logger.info("Disconnected from Redis")
    
    def get_value(self, key: str):
        if not key: raise ValueError("Key is required")
        return self.redis_client.get(key)
    
    def set_value(self, key: str, value: str, ttl: int | None = None):
        if not key or not value:  raise ValueError("Key and value are required")
        if ttl: self.redis_client.set(key, value, ex=ttl)
        else: self.redis_client.set(key, value)
    
    def if_exists(self, key: str):
        if not key: raise ValueError("Key is required")
        return self.redis_client.exists(key)
    
    def get_redis_client(self):
        return self.redis_client
    
    def set_dict(self, key: str, value: dict, ttl: int | None = None):
        if not key or not value: raise ValueError("Key and value are required")
        self.redis_client.hmset(key, value)
        if ttl: self.redis_client.expire(key, ttl)
    
    def get_dict(self, key: str):
        if not key:  raise ValueError("Key is required")
        return self.redis_client.hgetall(key)


# Connecting to a redis instance with SSM Param Store credential provider.
creds_provider = SecretsManagerProvider(secret_id=redis_settings.credentials_ssm_parameter)
redis_connector = RedisConnector(host=redis_settings.host, port=redis_settings.port, credential_provider=creds_provider)


if __name__ == "__main__":
    # Connecting to a redis instance with SSM Param Store credential provider.
    creds_provider = SecretsManagerProvider(secret_id=redis_settings.credentials_ssm_parameter)
    redis_connector = redis.Redis(host=redis_settings.host, port=redis_settings.port, credential_provider=creds_provider)
    redis_connector.ping()

    # Connecting to a redis instance with ElastiCache IAM credential provider.
    # username = "dev"
    # cluster_name = redis_settings.host
    # creds_provider = ElastiCacheIAMProvider(user=username, cluster_name=endpoint)
    # redis_connector = redis.Redis(host=redis_settings.host, port=redis_settings.port, credential_provider=creds_provider)
    # redis_connector.ping()