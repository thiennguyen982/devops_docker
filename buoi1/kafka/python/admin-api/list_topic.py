from confluent_kafka.admin import AdminClient

# Configuration
kafka_broker = 'localhost:9092'

# Create Kafka admin client
admin_client = AdminClient({'bootstrap.servers': kafka_broker})

# List all topics
try:
    metadata = admin_client.list_topics(timeout=10)
    topics = metadata.topics
    print("Topics in the Kafka cluster:")
    for topic in topics:
        print(topic)
except Exception as e:
    print(f"Failed to list topics: {e}")
