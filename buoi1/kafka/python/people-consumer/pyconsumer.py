import json
from dotenv import load_dotenv
import os
import logging
from confluent_kafka import Consumer, TopicPartition
from confluent_kafka.cimpl import OFFSET_END
import signal
import sys
import threading
import time

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__file__)

load_dotenv(verbose=True)

consumer = None
shutdown_event = threading.Event()

def shutdown_signal_handler(signum, frame):
    print("Shutdown Detected")
    shutdown_event.set()
    sys.exit(0)
    
def consume_message():
    while not shutdown_event.is_set():
        record = consumer.poll(1.0)
        
        if record is None:
            continue
        
        if record.error():
            logger.error(f"Consumer error: {record.error()}")
            continue

        logger.info(f"""
                    Consumed Information:
                    - Key: {record.key()}
                    - Information: {record.value()}
                    - Partition: {record.partition()}
                    - Offset: {record.offset()}
        """)
        
        # Manually commit the offset
        consumer.commit(offsets=[TopicPartition(record.topic(), record.partition(), record.offset() + 1)])
        
        time.sleep(1)
        
def on_assign(consumer, partitions):
    for tp in partitions:
        try:
            logger.info(f"Assigned - Topic: {tp.topic}, Partition: {tp.partition}, Offset: {consumer}")
        except Exception as e:
            logger.error(str(e))

def on_revoke(consumer, partitions):
    for tp in partitions:
        try:
            logger.info(f"Revoked - Topic: {tp.topic}, Partition: {tp.partition}, Offset: {consumer}")
        except Exception as e:
            logger.error(str(e))
            
def main():
    
    global consumer
    
    topic = os.environ['TOPICS_PEOPLE_BASIC_NAME']

    logger.info(f"""
                Started Python Consumer:
                - Topic: {topic}
                """)
    
    consumer = Consumer({
        'bootstrap.servers': os.environ['BOOTSTRAP_SERVERS'],
        'group.id': os.environ['CONSUMER_GROUP'],
        'enable.auto.commit': False,
        'auto.offset.reset': 'earliest'
    })
    
    consumer.subscribe([topic], on_assign=on_assign, on_revoke=on_revoke)
    
    
    try:
        consume_message_thread = threading.Thread(target=consume_message)
        consume_message_thread.start()
        
        # Periodically check the shutdown event
        while not shutdown_event.is_set():
            time.sleep(0.5)
                
        # Ensure the consumer joins the processing before exiting
        consume_message_thread.join()
        
        raise NotImplementedError
        
    except Exception as e:
        logging.error(str(e))

    finally:
        if consumer:
            consumer.close()
        print("Close consumer by the finally block")

if __name__ == "__main__":
    
    signal.signal(signal.SIGINT, shutdown_signal_handler)
    signal.signal(signal.SIGTERM, shutdown_signal_handler)
    
    main()