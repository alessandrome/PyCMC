from dataclasses import dataclass
from typing import Optional, List
from decimal import Decimal
from PyCMC.models import APIModel


@dataclass
class Platform(APIModel):
    id: int
    name: str
    symbol: str
    slug: str
    token_address: str


@dataclass
class Urls(APIModel):
    website: List[str]
    technical_doc: List[str]
    twitter: List[str]
    reddit: List[str]
    message_board: List[str]
    announcement: List[str]
    chat: List[str]
    explorer: List[str]
    source_code: List[str]


@dataclass
class CryptoInfo(APIModel):
    id: int
    name: str
    symbol: str
    category: str
    slug: str
    logo: str
    description: str
    date_added: str  # Timestamp (ISO 8601)
    date_launched: str  # Timestamp (ISO 8601)
    notice: Optional[str]  # Markdown formatte
    tags: List[str]
    platform: Optional[Platform]
    self_reported_circulating_supply: Optional[Decimal]
    self_reported_market_cap: Optional[Decimal]
    self_reported_tags: Optional[List[str]]
    infinite_supply: bool
    urls: Urls
