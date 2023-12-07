"""RPC server for membership"""
import pika, os, logging, threading, json
from rpc.channel_connection import rabbit_connect
from users.models import LeluUser
from users.serializers import WebsiteUserSerializer

log = logging.getLogger(__name__)


class RPCMembership:
    """RPC server for membership"""

    def __init__(self):
        self.channel = rabbit_connect()

    def get_lelu_user(self, email_members):
        uuid_members = ""
        email_members = email_members.split(" ")
        for email in email_members:
            user, _ = LeluUser.objects.get_or_create(email=email)
            uuid_members += " " + user.uuid.hex
        return uuid_members.strip()

    def _on_request(self, ch, method, props, body):
        email_members = body.decode('utf-8')
        uuid_members = self.get_lelu_user(email_members)
        ch.basic_publish(exchange='',
                         routing_key=props.reply_to,
                         properties=pika.BasicProperties(correlation_id= \
                                                             props.correlation_id),
                         body=uuid_members)
        ch.basic_ack(delivery_tag=method.delivery_tag)

    def start(self):
        self.channel.queue_declare(queue='auth.membership')
        self.channel.basic_qos(prefetch_count=1)
        self.channel.basic_consume(queue='auth.membership',
                                   on_message_callback=self._on_request)

        log.info("Awaiting RPC Membership")
        consumer = threading.Thread(target=self.channel.start_consuming)
        consumer.daemon = True
        consumer.start()
