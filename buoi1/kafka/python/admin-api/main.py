import os
from dotenv import load_dotenv
from fastapi import FastAPI
from confluent_kafka import KafkaException
from confluent_kafka.error import KafkaError
from confluent_kafka.admin import AdminClient, NewTopic, ConfigResource
import logging

logger = logging.getLogger()

load_dotenv(verbose=True)

print(os.environ['BOOTSTRAP_SERVERS'])

app = FastAPI()

@app.on_event('startup')
async def startup_event():
    client = AdminClient({'bootstrap.servers': os.environ['BOOTSTRAP_SERVERS']})
    topics = [
        NewTopic(
            topic=os.environ['TOPICS_PEOPLE_BASIC_NAME'],
            num_partitions=int(os.environ['TOPICS_PEOPLE_BASIC_PARTITIONS']),
            replication_factor=int(os.environ['TOPICS_PEOPLE_BASIC_REPLICAS'])
        ),
        NewTopic(
            topic=f"{os.environ['TOPICS_PEOPLE_BASIC_NAME']}-short",
            num_partitions=int(os.environ['TOPICS_PEOPLE_BASIC_PARTITIONS']),
            replication_factor=int(os.environ['TOPICS_PEOPLE_BASIC_REPLICAS']),
            config={
                'retention.ms': '3600000'
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

@app.get('/hello-world')
async def hello_world():
    return {"message": "hello-world"}