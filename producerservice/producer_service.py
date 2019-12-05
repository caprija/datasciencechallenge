import logging
import ijson
from kafka_producer import KafkaProducerService

class ProducerService(object):
    """
    This class serves as to read user events from a Json file using iterative parser ijson
    """

    def __init__(self, topic):
        logging.basicConfig(level=logging.INFO)
        logging.info('Call ProducerService')
        self._topic = topic

    def parse_json_file(self):
        """
        Read json file by using ijson which read efficiently large python files and send user object to kafka topic
        named user
        :return: none
        :rtype: none
        """
        with open('MOCK_DATA.json') as json_file:
            for object in ijson.items(json_file, 'item'):
                KafkaProducerService.send(self._topic, object)


if __name__ == '__main__':
	# we can also use argparser to get the arguments like topic here from user.
    producer_service = ProducerService("user")
    producer_service.parse_json_file()


