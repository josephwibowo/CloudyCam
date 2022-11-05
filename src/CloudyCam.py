import io

import requests
import urllib.parse

import packets
import proto.HelloContainer_pb2 as hc
import proto.TokenContainer_pb2 as tc
from logger import log


def get(url, headers=None):
    response = requests.get(url, headers=headers, timeout=5)
    response.raise_for_status()
    return response


def post(url, headers=None, data=None):
    response = requests.post(url, headers=headers, data=data, timeout=6)
    response.raise_for_status()
    return response


class CloudyCam:
    def __init__(self, config, limit=500):
        self.config = config
        self.camera = {}
        self.token_container = tc.TokenContainer()
        self.hello_container = self._init_hello_container()
        self.video_channel_id = None
        self.audio_channel_id = None
        self.video_stream = []
        self.audio_stream = []
        self.stream_limit = config.get('stream_limit', limit)
        self.stream_host = ''


    def _init_hello_container(self):
        helloRequestBuffer = hc.HelloContainer()
        helloRequestBuffer.ProtocolVersion = 3
        helloRequestBuffer.RequireConnectedCamera = False
        helloRequestBuffer.UserAgent = self.config['user_agent']
        helloRequestBuffer.ClientType = 3
        return helloRequestBuffer


    def _get_access_token(self):
        headers = {
            "Sec-Fetch-Mode": "cors",
            "User-Agent": self.config['user_agent'],
            "X-Requested-With": "XmlHttpRequest",
            "Referer": "https://accounts.google.com/o/oauth2/iframe",
            "cookie": self.config['cookie']
        }
        r = get(self.config['auth_url'], headers).json()
        if 'access_token' not in r:
            raise requests.RequestException(f"Google request error. Response: {r}")
        return r['access_token']


    def _get_ss_domain(self):
        auth_url_parse = urllib.parse.urlparse(self.config['auth_url'])
        ss_domain = urllib.parse.parse_qs(auth_url_parse.query).get('ss_domain')[0]
        return ss_domain


    def _get_jwt_token(self, access_token):
        url = 'https://nestauthproxyservice-pa.googleapis.com/v1/issue_jwt'
        headers = {
            "Authorization": f"Bearer {access_token}",
            "User-Agent": self.config['user_agent'],
            "x-goog-api-key": self.config['api_key'],
            "Referer": self._get_ss_domain()
        }
        data = {
            'embed_google_oauth_access_token': 'true',
            'expire_after': '3600s',
            'google_oauth_access_token': f"{access_token}",
            'policy_id': 'authproxy-oauth-policy'
        }
        r = post(url, headers=headers, data=data)
        return r.json()['jwt']


    def get_camera(self):
        log.info('getting tokens')
        token = self._get_access_token()
        jwt = self._get_jwt_token(token)
        log.info('tokens obtained')
        cam_url = f"{self.config['camera_api_hostname']}/api/cameras.get_owned_and_member_of_with_properties"
        cam_headers = {
            'Cookie': f"user_token={jwt}",
            "User-Agent": self.config['user_agent'],
            "Referer": self.config['nest_api_hostname']
        }
        r3 = get(cam_url, headers=cam_headers)
        log.info('camera obtained')
        self.camera = r3.json()['items'][0]
        self.token_container.OliveToken = jwt
        token_stream = io.BytesIO(self.token_container.SerializeToString())
        self.hello_container.Uuid = self.camera['uuid']
        self.hello_container.AuthorizeRequest.append(token_stream.getvalue())
        hello_stream = io.BytesIO(self.hello_container.SerializeToString())
        self.hello_buffer = packets.preformat_data(packets.PACKET_TYPES['HELLO'], bytearray(hello_stream.getvalue()))
