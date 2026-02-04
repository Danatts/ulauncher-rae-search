import logging
import requests
from api_types import Definition, ErrorResponse, RateLimitExceededResponse, WordEntryResponse, WordEntry
from typing import List

logger = logging.getLogger(__name__)

class RAEAPI:
    def __init__(self):
        self.base_url = 'https://rae-api.com/api/words/'
        self.headers = {
            'Accept': 'application/json'
        }

    def search_word(
            self, word: str,
            max_results: int = 5
    ) -> List[Definition] | None:
        """Search for a word in the RAE dictionary"""
        try:
            word = word.strip().lower()
            url = f'{self.base_url}{word}'
            response = requests.get(
                url,
                headers=self.headers,
                timeout=10
            )

            if response.status_code == 404:
                error_respone: ErrorResponse = response.json()
                logger.error(f'Request error: {error_respone.get('error')}.')
                return []

            if response.status_code == 429:
                rate_limit: RateLimitExceededResponse = response.json()
                logger.error(f'Request error: {rate_limit.get('error')}.')
                return []

            entry_response: WordEntryResponse = response.json()

            if not entry_response.get('ok'):
                logger.error(f'Request error: word entry data false.')
                return []

            return self.get_word_senses(entry_response.get('data'), max_results)

        except requests.exceptions.RequestException as e:
            logger.error(f'Connection error: {str(e)}')
            return None

        except Exception as e:
            logger.error(f'Unexpected error: {str(e)}')
            return None
    
    def get_word_senses(
            self,
            word_entry: WordEntry,
            max_results: int
    ) -> List[Definition]:
        meanings = word_entry.get('meanings', [])
        if not meanings:
            return []

        senses = meanings[0].get('senses', [])
        if not meanings:
            return []

        return senses[:max_results]
