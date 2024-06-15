import json
from dotenv import load_dotenv
import os
import logging
from confluent_kafka import Consumer
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
    shutdown_event.set() # Signal that shutdown is requested
    if consumer:
        consumer.close()
    print("Consumer Closed")
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

def main():
    global consumer
    
    logger.info(f"""
                Started Python Consumer:
                - Topic: {os.environ['TOPICS_PEOPLE_BASIC_NAME']}
                """)
    
    consumer = Consumer({
        'bootstrap.servers': os.environ['BOOTSTRAP_SERVERS'],
        'group.id': os.environ['CONSUMER_GROUP'],
        'auto.offset.reset': 'latest'
    })
    
    consumer.subscribe([
        os.environ['TOPICS_PEOPLE_BASIC_NAME']
    ])
    
    try:
        consume_message_thread = threading.Thread(target=consume_message)
        consume_message_thread.start()
        
       # Periodically check the shutdown event
        while not shutdown_event.is_set():
            time.sleep(0.5)
        
        # Ensure the consumer joins the processing before exiting
        consume_message_thread.join()
            
    except Exception as e:
        logging.error(str(e))

    finally:
        if consumer:
            consumer.close()

if __name__ == "__main__":
    
    signal.signal(signal.SIGINT, shutdown_signal_handler)
    signal.signal(signal.SIGTERM, shutdown_signal_handler)
    
    main()