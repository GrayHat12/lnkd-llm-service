import os
import pika


class QueueService:
    def __init__(self, queue_name: str):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(os.environ["QUEUE_URI"]))
        self.channel = self.connection.channel()
        self.queue_name = queue_name
        self.channel.queue_declare(queue=queue_name)

class QueuePublishService(QueueService):
    def publish(self, message: str):
        return self.channel.basic_publish(exchange="", routing_key=self.queue_name, body=message)