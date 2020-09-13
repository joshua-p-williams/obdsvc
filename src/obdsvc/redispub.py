import redis
import json

class RedisPub:
  """Publishes OBD data onto redis"""

  def __init__(self, redishost):
    """Default constructor accepting parameters for creating a conection to redis"""

    self._redis = redis.Redis(host=redishost, port=6379, db=0)
  
  def publishResponse(self, name, response):
    """Constructs a message and pushes to redis cache and pubsub channel by the name"""
    
    value = {
      'message': str(response),
      'value': str(response.value),
      'units': None,
      'magnitude': None,
    }

    if hasattr(response.value, 'units'):
      value['units'] = str(response.value.units)
      value['magnitude'] = str(response.value.magnitude)

    self._redis.set(name, json.dumps(value))
    self._redis.publish(name, json.dumps(value))
