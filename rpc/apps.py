# pylint: skip-file
from django.apps import AppConfig
from django.conf import settings
import os, time


class RpcConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'rpc'

    def ready(self):
        if settings.RPC_SERVERS_START:
            from rpc.websiteuser_register import RPCWebUserReg
            from rpc.membership import RPCMembership
            RPCWebUserReg().start()
            RPCMembership().start()
