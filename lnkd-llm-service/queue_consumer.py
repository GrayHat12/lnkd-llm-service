import pika
import traceback
from pika.channel import Channel
import pika.spec
from pymongo import ReturnDocument
from llm_service import prompt_llm
from db import lnkd_requests_collection

connection = pika.BlockingConnection(pika.ConnectionParameters("rabbitmq"))
channel = connection.channel()

class QueueService:
    def __init__(self, queue_name: str):
        self.queue_name = queue_name
        channel.queue_declare(queue=queue_name)

class QueueConsumerService(QueueService):

    def __init__(self, queue_name):
        super().__init__(queue_name)
        channel.basic_consume(queue="llm_queue", auto_ack=False, on_message_callback=self.on_message)

    def on_message(self, channel: Channel, method: pika.spec.Basic.Deliver, properties: pika.spec.BasicProperties, body: bytes):
        try:
            doc = lnkd_requests_collection().find_one_and_update({
                "lnkd_request_id": body.decode(),
                "status": 3
            }, {
                "$set": {
                    "status": 4,
                    "status_message": "Prompting LLM"
                }
            }, return_document=ReturnDocument.AFTER, upsert=False)
            if not doc:
                print(f"Something went wrong, {body=} not found in db")
                channel.basic_ack(method.delivery_tag)
                return
            message = prompt_llm(doc)
            doc = lnkd_requests_collection().update_one({
                "lnkd_request_id": body.decode(),
            }, {
                "$set": {
                    "status": 5,
                    "status_message": "Message Generated",
                    "message": message
                }
            }, upsert=False)
            channel.basic_ack(method.delivery_tag)
        except:
            traceback.print_exc()
            channel.basic_reject(method.delivery_tag)
            doc = lnkd_requests_collection().update_one({
                "lnkd_request_id": body.decode(),
            }, {
                "$set": {
                    "status": 6,
                    "status_message": "Something went wrong when in the prompt service",
                    "message": None
                }
            }, upsert=False)

    def start_consuming(self):
        channel.basic_qos(prefetch_count=1)
        channel.start_consuming()
    
    def stop_consuming(self):
        channel.stop_consuming()