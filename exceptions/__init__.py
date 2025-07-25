from typing import Optional

import requests

from PyCMC.models.status import Status


class CoinMarketCapError(Exception):
    message: str = "CoinMarketCap Error"


class CoinMarketCapAPIError(Exception):
    """Base class for all CoinMarketCap API errors."""
    response: requests.Response
    status: Optional[Status] = None

    def __init__(self, response: requests.Response, message: str = "CoinMarketCap API error",
                 status: Optional[Status] = None):
        super().__init__(message)
        self.response = response
        self.message = message
        self.status = status


class CMCTooManyRequestsException(CoinMarketCapAPIError):
    pass



class CMCBadRequestException(CoinMarketCapAPIError):
    pass


class CMCUnauthorizedException(CoinMarketCapAPIError):
    pass


class CMCForbiddenException(CoinMarketCapAPIError):
    pass


class CMCInternalServerErrorException(CoinMarketCapAPIError):
    pass
