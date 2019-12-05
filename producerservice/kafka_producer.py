import logging
import json
from kafka import KafkaProducer, SimpleProducer, KafkaClient


class KafkaProducerService(object):
    def send(topic, payload):
        """
        Get the Spark Dataframe and convert date in a provided date format.
    
        :param topic: kafka topic name to send user data
        :type topic: string
        :param payload: user json object
        :type payload: json
        :return: none
        :rtype: none
        """
        try:
            BOOTSTRAP_SERVERS_CONFIG = "kafka:9092"
            client_id = "user_message_producer"
            # value_serializer = lambda m: json.dumps(m).encode('ascii')
            payload = json.dumps(payload).encode('utf-8')
            logging.info('Send User Info to Kafka Topic')
            producer = KafkaProducer(bootstrap_servers=BOOTSTRAP_SERVERS_CONFIG)
            producer.send(topic, payload)
            producer.flush()
        except Exception as error:
            print(error)
            raise
    	
