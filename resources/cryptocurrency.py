import requests
from requests import Response

import PyCMC
import PyCMC.CMCConnector
from PyCMC.endpoints import Endpoints
from PyCMC.models.result import Result
from PyCMC.models.status import Status
from PyCMC.models import crypto


class Cryptocurrency:
    endpoint = "cryptocurrency"

    def __init__(self, api_wrapper):
        self.api_wrapper = api_wrapper # type: PyCMC.CMCConnector.CoinMarketCapAPI

    def info(self) -> (Result, Response):
        http_response = self.api_wrapper.request([self.api_wrapper.BASE_URL, self.endpoint], version='v2')
        status = Status(**http_response['status'])
        data = http_response['data']
        result = Result(status, {})
        for k, el in data:
            result.data[int(k)] = crypto.CryptoInfo.from_api_response(el)
        return result, http_response
