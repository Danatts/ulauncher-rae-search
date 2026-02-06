from typing import List, TypedDict
from enum import Enum

class SearchStatus(Enum):
    OK = 'ok'
    NOT_FOUND = 'not_found'
    NETWORK_ERROR = 'network_error'
    RATE_LIMIT = 'rate_limit'
    API_ERROR = 'api_error'

class Conjugation(TypedDict):
    non_personal: str
    indicative: str
    subjunctive: str
    imperative: str

class Article(TypedDict):
    category: str
    gender: str

class Definition(TypedDict):
    raw: str
    meaning_number: int
    category: str
    verb_category: str
    gender: str
    article: Article
    usage: str
    description: str
    synonyms: List[str]
    antonyms: List[str]

class Origin(TypedDict):
    raw: str
    type: str
    voice: str
    text: str

class Meaning(TypedDict):
    origin: Origin
    senses: List[Definition]
    conjugations: Conjugation

class WordEntry(TypedDict):
    word: str
    meanings: List[Meaning]

class WordEntryResponse(TypedDict):
    ok: bool
    data: WordEntry

class ErrorResponse(TypedDict):
    ok: bool
    error: str
    suggestions: List[str]

class RateLimitExceededResponse(TypedDict):
    ok: bool
    error: str
    message: str
    retry_after: int

class SearhResult(TypedDict, total=False):
    status: SearchStatus
    data: List[Definition]
    suggestions: List[str]
    retry_after: int
    message: str

