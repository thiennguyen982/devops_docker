from confluent_kafka.admin import AdminClient, NewTopic

def create_kafka_topic(broker, topic_name, num_partitions, replication_factor):
    # Create Kafka admin client
    admin_client = AdminClient({'bootstrap.servers': broker})

    # Define the new topic
    topic = NewTopic(topic=topic_name,
                     num_partitions=num_partitions,
                     replication_factor=replication_factor)

    # Create the topic
    futures = admin_client.create_topics([topic])

    # Wait for each operation to finish
    for topic, future in futures.items():
        try:
            future.result()  # The result itself is None
            print(f"Topic '{topic}' created successfully.")
        except Exception as e:
            print(f"Failed to create topic '{topic}': {e}")

if __name__ == "__main__":
    broker = 'localhost:9092'
    topic_name = 'my-new-topic'
    num_partitions = 1
    replication_factor = 1

    create_kafka_topic(broker, topic_name, num_partitions, replication_factor)
