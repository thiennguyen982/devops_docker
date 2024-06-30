from typing import List
from confluent_kafka import SerializingProducer
from confluent_kafka.schema_registry.avro import AvroSerializer
from confluent_kafka.schema_registry import SchemaRegistryClient
from confluent_kafka.serialization import StringSerializer
from confluent_kafka import SerializingProducer
from confluent_kafka.admin import AdminClient, NewTopic
from fastapi import FastAPI
from faker import Faker
from dotenv import load_dotenv
from models import Person, SuccessHandler
from commands import CreatePeopleCommand
import logging
import os
import schemas

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__file__)

load_dotenv(verbose=True)

def make_producer() -> SerializingProducer:
    #Make Schema_Registry Client
    schema_reg_client = SchemaRegistryClient({
        'url': os.environ['SCHEMA_REGISTRY_URL']
    })
    
    #Create AvroSerializer
    avro_serializer = AvroSerializer(
        schema_reg_client,
        schemas.person_value_v2,
        lambda person, ctx: person.dict()
    )
    
    #Create & Return SerializingProducer
    return SerializingProducer({
        "bootstrap.servers": os.environ['BOOTSTRAP_SERVERS'],
        "linger.ms": 300,
        "enable.idempotence": "true",
        "max.in.flight.requests.per.connection": 1,
        "acks": "all",
        "key.serializer": StringSerializer('utf_8'),
        "value.serializer": avro_serializer,
        "partitioner": "murmur2_random"
    })
    
app = FastAPI()
    
@app.on_event("startup")
async def startup_event():
    client = AdminClient({
        'bootstrap.servers': os.environ['BOOTSTRAP_SERVERS']
    })
    
    topic = NewTopic(
        topic=os.environ['TOPICS_PEOPLE_AVRO_NAME'],
        num_partitions=int(os.environ['TOPICS_PEOPLE_AVRO_PARTITIONS']),
        replication_factor=int(os.environ['TOPICS_PEOPLE_AVRO_REPLICAS'])
    )
    
    try:
        futures = client.create_topics([topic])
        for topic_name, future in futures.items():
            future.result()
            logger.info(f"Topic {topic_name} created!")
    except Exception as e:
        logger.warning(str(e))
        
@app.post("/api/people", status_code=201, response_model=List[Person])
async def create_people(cmd : CreatePeopleCommand):
    people : List[Person] = []
    faker = Faker()
    
    producer = make_producer()
    
    for _ in range(cmd.count):
        person = Person(
            first_name=faker.first_name(),
            last_name=faker.last_name(),
            title=faker.job()
        )
        
        people.append(person)
        
        try:
            producer.produce(
                topic=os.environ['TOPICS_PEOPLE_AVRO_NAME'],
                key=person.title.lower().replace(r's+', '-'),
                value=person, 
                on_delivery=SuccessHandler(person=person)
            )
        except Exception as e:
            logger.error(str(e))
        
    producer.flush()
    
    return people