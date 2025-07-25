import requests

from PyCMC.exceptions import *
from PyCMC.models.status import Status


class CoinMarketCapAPI:
    BASE_URL = 'https://pro-api.coinmarketcap.com/{}'

    def __init__(self, api_key):
        self._api_key = api_key
        self._session = requests.Session()
        self._session.headers.update({"X-CMC_PRO_API_KEY": self._api_key, 'Accept': 'application/json'})

    def prepare_request(self, endpoint_uri, params=None, data=None, version: str = 'v1'):
        url = self.BASE_URL.format(version)
        if type(url) is str:
            url += endpoint_uri
        elif type(url) is list:
            url += '/'.join(endpoint_uri)
        else:
            raise TypeError('endpoint_uri must be str or list')

        request = requests.Request(method='GET', url=url, data=data, params=params)
        return self._session.prepare_request(request)

    def send_request(self, request: requests.PreparedRequest):
        try:
            response = self._session.send(request)
            response.raise_for_status()
            return response
        except requests.exceptions.HTTPError as e:
            result = e.response.json()
            status = None
            if 'status' in result:
                status = Status(**result['status'])
                msg = status.error_message if status else f"Request failed: {e}"
                if status.error_code == 400:
                    raise CMCBadRequestException(response=e.response, message=msg, status=status) from e
                if status.error_code == 401:
                    raise CMCUnauthorizedException(response=e.response, message=msg, status=status) from e
                if status.error_code == 403:
                    raise CMCForbiddenException(response=e.response, message=msg, status=status) from e
                if status.error_code == 429:
                    raise CMCTooManyRequestsException(response=e.response, message=msg, status=status) from e
                if status.error_code == 500:
                    raise CMCInternalServerErrorException(response=e.response, message=msg, status=status) from e
            raise

    def request(self, endpoint_uri, params=None, data=None, version: str = 'v1'):
        return self.send_request(self.prepare_request(endpoint_uri, params=params, data=data, version=version))

    def set_api_key(self, api_key):
        self._api_key = api_key
        self._session.headers.update({"X-CMC_PRO_API_KEY": self._api_key})
