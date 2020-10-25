import os
import logging
from requests_oauthlib import OAuth1
from rauth import OAuth1Service

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(lineno)d - %(message)s', level=logging.DEBUG)
logger = logging.getLogger(__name__)

try:
    CONSUMER_KEY = os.environ['OSM_CONSUMER_KEY']
    CONSUMER_SECRET = os.environ['OSM_CONSUMER_SECRET']
except KeyError:
    exit()


class Authorisation:

    def __init__(self):
        self.osm_auth = OAuth1Service(
            name='osm',
            consumer_key=CONSUMER_KEY,
            consumer_secret=CONSUMER_SECRET,
            request_token_url='https://master.apis.dev.openstreetmap.org/oauth/request_token',
            access_token_url='https://master.apis.dev.openstreetmap.org/oauth/access_token',
            authorize_url='https://master.apis.dev.openstreetmap.org/oauth/authorize',
            base_url='https://master.apis.dev.openstreetmap.org')

    def request_token(self):
        self.request_token, self.request_token_secret = self.osm_auth.get_request_token()
        authorize_url = self.osm_auth.get_authorize_url(self.request_token)
        return authorize_url

    def authorize(self):
        acc_token, acc_token_secret = self.osm_auth.get_access_token(self.request_token, self.request_token_secret)
        auth_token = OAuth1(self.osm_auth.consumer_key, self.osm_auth.consumer_secret, acc_token, acc_token_secret)
        return auth_token

    @staticmethod
    def cr_auth_token(auth_token, auth_secret):
        return OAuth1(CONSUMER_KEY, CONSUMER_SECRET, auth_token, auth_secret)

