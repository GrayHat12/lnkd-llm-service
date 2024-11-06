import os
import pika

connection = pika.BlockingConnection(pika.ConnectionParameters(os.environ["QUEUE_URI"]))
channel = connection.channel()


class QueueService:
    def __init__(self, queue_name: str):
        self.queue_name = queue_name
        channel.queue_declare(queue=queue_name)

class QueuePublishService(QueueService):
    def publish(self, message: str):
        return channel.basic_publish(exchange="", routing_key=self.queue_name, body=message)