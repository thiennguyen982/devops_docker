import json
import logging
import os
from dotenv import load_dotenv
from confluent_kafka import Consumer, KafkaError, TopicPartition
import time


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv(verbose=True)


def people_key_deserializer(key):
    return key.decode('utf-8')


def people_value_deserializer(value):
    return json.loads(value.decode('utf-8'))


def main():
    logger.info(f"""
    Started Python Consumer
    for topic {os.environ['TOPICS_PEOPLE_BASIC_NAME']}
  """)

    conf = {
        'bootstrap.servers': os.environ['BOOTSTRAP_SERVERS'],
        'group.id': os.environ['CONSUMER_GROUP'],
        'auto.offset.reset': 'earliest'  # Adjust this as needed
    }

    consumer = Consumer(conf)
    consumer.subscribe([os.environ['TOPICS_PEOPLE_BASIC_NAME']])

    try:
        while True:
            msg = consumer.poll(timeout=1.0)
            if msg is None:
                continue
            if msg.error():
                if msg.error().code() == KafkaError._PARTITION_EOF:
                    # End of partition, consumer has reached end
                    continue
                else:
                    # Handle other errors
                    logger.error(msg.error())
                    break

            logger.info(f"""
            Consumed person {msg.value()}
            with key '{msg.key().decode('utf-8')}'
            from partition {msg.partition()}
            at offset {msg.offset()}
            """)

            # Manually commit offset
            consumer.commit(offsets=[TopicPartition(msg.topic(), msg.partition(), msg.offset() + 1)])
            
            time.sleep(5)
            
            

    except KeyboardInterrupt:
        pass
    finally:
        # Close consumer on exit
        consumer.close()


if __name__ == '__main__':
    main()
