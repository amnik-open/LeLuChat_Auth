"""RPC server for registering WebsiteUser"""
import pika
import logging
import threading
import json
from rpc.channel_connection import rabbit_connect
from users.models import WebsiteUser
from users.serializers import WebsiteUserSerializer

log = logging.getLogger(__name__)


class RPCWebUserReg:
    """RPC server for registering WebsiteUser"""

    def __init__(self):
        self.channel = rabbit_connect()

    def _register(self, name):
        wu = WebsiteUser.objects.create(name=name)
        serializer = WebsiteUserSerializer(wu)
        return serializer.data

    def _on_request(self, ch, method, props, body):
        wu = self._register(str(body.decode('utf-8')))
        ch.basic_publish(exchange='',
                         routing_key=props.reply_to,
                         properties=pika.BasicProperties(correlation_id= \
                                                             props.correlation_id),
                         body=json.dumps(wu))
        ch.basic_ack(delivery_tag=method.delivery_tag)

    def start(self):
        self.channel.queue_declare(queue='auth.webuser.register')
        self.channel.basic_qos(prefetch_count=1)
        self.channel.basic_consume(queue='auth.webuser.register',
                                   on_message_callback=self._on_request)

        log.info("Awaiting RPC WebsiteUser registeration")
        consumer = threading.Thread(target=self.channel.start_consuming)
        consumer.daemon = True
        consumer.start()
