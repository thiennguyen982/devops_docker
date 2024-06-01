from confluent_kafka.admin import AdminClient, NewTopic, NewPartitions, ConfigResource, ConfigSource

def list_kafka_topics(admin_client):
    """List all topics in the Kafka cluster."""
    try:
        metadata = admin_client.list_topics(timeout=10)
        topics = metadata.topics
        return list(topics.keys())
    except Exception as e:
        print(f"Failed to list topics: {e}")
        return []

def delete_kafka_topics(admin_client, topics):
    """Delete specified topics in the Kafka cluster."""
    if not topics:
        print("No topics to delete.")
        return

    futures = admin_client.delete_topics(topics, operation_timeout=30)

    # Wait for each operation to finish
    for topic, future in futures.items():
        try:
            future.result()  # The result itself is None
            print(f"Topic '{topic}' deleted successfully.")
        except Exception as e:
            print(f"Failed to delete topic '{topic}': {e}")

if __name__ == "__main__":
    broker = 'localhost:9092'

    # Create Kafka admin client
    admin_client = AdminClient({'bootstrap.servers': broker})

    # List all topics
    # topics = list_kafka_topics(admin_client)
    topics = ["my-new-topic"]
    print(f"Topics to be deleted: {topics}")

    # Delete all topics
    delete_kafka_topics(admin_client, topics)