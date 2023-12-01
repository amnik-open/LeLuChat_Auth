"""Define Rest Authentication class for WebsiteUser"""
from rest_framework.authentication import TokenAuthentication
from users.models import WebsiteUserToken

class WebsiteUserTokenAuthentication(TokenAuthentication):
    """Authentication clss for WebsiteUser"""

    model = WebsiteUserToken
