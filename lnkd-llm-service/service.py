from queue_consumer import QueueConsumerService

if __name__ == "__main__":
    queue_service = QueueConsumerService("llm_queue")

    queue_service.start_consuming()