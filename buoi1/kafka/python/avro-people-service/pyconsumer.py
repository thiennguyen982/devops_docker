from dotenv import load_dotenv
from confluent_kafka import DeserializingConsumer
from confluent_kafka.schema_registry import SchemaRegistryClient
from confluent_kafka.schema_registry.avro import AvroDeserializer
from confluent_kafka.serialization import StringDeserializer
import schemas
from models import Person
import logging
import os

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__file__)

load_dotenv(verbose=True)

def make_consumer() -> DeserializingConsumer:
    #Create SchemaRegistryClient
    schema_reg_client = SchemaRegistryClient({
        'url': os.environ['SCHEMA_REGISTRY_URL']
    })
    
    #Create AvroDeserializer
    avro_deserializer = AvroDeserializer(
        schema_reg_client,
        schemas.person_value_v1,
        lambda data, ctx : Person(**data)
    )
    
    #Create And Return DeserializingConsumer
    return DeserializingConsumer({
        'bootsrap.servers': os.environ['BOOTSTRAP_SERVERS'],
        'key.deserializer': StringDeserializer('utf-8'),
        'value.deserializer': avro_deserializer,
        'group.id': os.environ['CONSUMER_GROUP'],
        'enable.auto.commit': 'false'
    })

def main():
    logger.info(f"""
                Starting Python Avro Consumer:
                -Topic: {os.environ['TOPICS_PEOPLE_AVRO_NAME']}
                """)
    
    consumer = make_consumer()
    consumer.subscribe([os.environ['TOPICS_PEOPLE_AVRO_NAME']])
    
    while True:
        msg = consumer.poll(1.0)
        if msg is not None:
            person = msg.value()
            logger.info(f"""
                        """)

if __name__ == "__main__":
    main()