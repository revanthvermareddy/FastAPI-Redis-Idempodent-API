import hashlib
import json

from loguru import logger

from app.services.redis.service import RedisConnector, redis_connector


class IdempotentAPI:
    def __init__(self, redis_connector: RedisConnector):
        self.redis_connector = redis_connector

    def make_request(self, request_body: dict, ttl=3600):
        # Calculate the idempotency key based on the request body
        idempotency_key = self._calculate_idempotency_key(request_body)
        
        # Check if the request has already been processed.
        if self.redis_connector.if_exists(key=idempotency_key):
            logger.info(f'idempotency_key: {idempotency_key} already exists, hence retreiving from the cache')
            
            # The request has already been processed, so return the stored response.
            return self.redis_connector.get_dict(key=idempotency_key)

        # The request has not been processed yet, so process it and store the response.
        response = self._process_request(request_body)
        logger.info(f'processed request successfully and got the response: {response}')
        
        # Store the response with a TTL
        self.redis_connector.set_dict(key=idempotency_key, value=response, ttl=ttl)
        logger.info(f'successfully set the response: {response} in redis for the idempotency_key: {idempotency_key} with ttl: {ttl} second(s)')

        return response

    def _process_request(self, request_body: dict):
        # Implement the request processing logic here.
        
        return {"status": "Success", "message": "Request processed successfully"}

    def _calculate_idempotency_key(self, request_body: dict):
        # Convert the request body to JSON and encode it to bytes
        request_body_bytes = json.dumps(request_body).encode('utf-8')

        # Calculate the SHA256 hash of the request body
        return hashlib.sha256(request_body_bytes).hexdigest()


# Create an idempotent API instance.
idempotent_api = IdempotentAPI(redis_connector)
