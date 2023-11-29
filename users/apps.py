"""This file include configuration for app"""
from django.apps import AppConfig


class UsersConfig(AppConfig):
    """Set config for users app"""

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'users'

    def ready(self):
        import users.signals
