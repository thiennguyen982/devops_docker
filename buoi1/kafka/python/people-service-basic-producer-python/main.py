from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
import os
import uuid
from confluent_kafka.admin import AdminClient, NewTopic, ConfigResource
from confluent_kafka import KafkaException
from confluent_kafka.error import KafkaError
from confluent_kafka import Producer
from commands import CreatePeopleCommand
from entities import Person, SuccessHandler
from typing import List
from faker import Faker

load_dotenv(verbose=True)

app = FastAPI()

def make_producer():
    try:
        return Producer({
            'bootstrap.servers': os.environ['BOOTSTRAP_SERVERS'],
            'linger.ms': int(os.environ['TOPICS_PEOPLE_ADV_LINGER_MS']),
            'retries': int(os.environ['TOPICS_PEOPLE_ADV_RETRIES']),
            'max.in.flight.requests.per.connection': int(os.environ['TOPICS_PEOPLE_ADV_INFLIGHT_REQS']),
            'acks': os.environ['TOPICS_PEOPLE_ADV_ACKS']
        })
    except Exception as e:
        print(str(e))
        return None
        
@app.on_event('startup')
async def startup_event():
    client = AdminClient({'bootstrap.servers': os.environ['BOOTSTRAP_SERVERS']})
    
    topics = [
        NewTopic(
            topic=os.environ['TOPICS_PEOPLE_BASIC_NAME'],
            num_partitions=int(os.environ['TOPICS_PEOPLE_BASIC_PARTITIONS']),
            replication_factor=int(os.environ['TOPICS_PEOPLE_BASIC_REPLICAS']),
        ),
        NewTopic(
            topic=f"{os.environ['TOPICS_PEOPLE_BASIC_NAME']}-short",
            num_partitions=int(os.environ['TOPICS_PEOPLE_BASIC_PARTITIONS']),
            replication_factor=int(os.environ['TOPICS_PEOPLE_BASIC_REPLICAS']),
            config={
                'retention.ms': '3600000'
            }
        ),
        NewTopic(
            topic=f"{os.environ['TOPICS_PEOPLE_ADV_NAME']}",
            num_partitions=int(os.environ['TOPICS_PEOPLE_ADV_PARTITIONS']),
            replication_factor=int(os.environ['TOPICS_PEOPLE_ADV_REPLICAS']),
            config={
                'retention.ms': '300'
            }
        )
    ]
    
    try:
        futures = client.create_topics(topics)
        
        for topic, future in futures.items():
            try:
                future.result()  # The result itself is None
                print(f"Topic '{topic}' created successfully.")
            except KafkaException as ke:
                if ke.args[0].code() == KafkaError.TOPIC_ALREADY_EXISTS:
                    print(f"Topic '{topic}' already exists.")
                    
        cfg_resource = ConfigResource(
            ConfigResource.Type.TOPIC, 
            os.environ['TOPICS_PEOPLE_BASIC_NAME'], 
            {
                'retention.ms': '3600000'
            }
        )
        
        client.alter_configs([cfg_resource])
        
    except Exception as e:
        print(f"Another Exception: {e}")
        
    finally:
        if client:
            client.close()

@app.post('/api/people', status_code=201, response_model=List[Person])
async def create_people(cmd : CreatePeopleCommand):
    people : List[Person] = []
    
    faker = Faker()
    producer = make_producer()
    
    if not producer:
        raise HTTPException(status_code=500, detail="Failed to create Kafka producer")
    
    for _ in range(cmd.count):
        person = Person(
            id=str(uuid.uuid4()),
            name=faker.name(),
            title=faker.job(),
            company=faker.company(),
            YOE=faker.random_int(min=1, max=24)
            
        )
        
        people.append(person)
        
        try:
            producer.produce(
                topic=os.environ['TOPICS_PEOPLE_BASIC_NAME'],
                key=person.title.lower().replace(' ', '-').encode('utf-8'),
                value=person.json().encode('utf-8'),
                callback=SuccessHandler(person)
            )
        except KafkaException as e:
            if e.args[0].code() == KafkaError._ALL_BROKERS_DOWN:
                return {"error": "Kafka brokers are down, unable to produce message"}, 500
        
    producer.flush()
    
    return people