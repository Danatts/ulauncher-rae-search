import logging
import requests
from api_types import Definition, WordEntryResponse, WordEntry
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
    ) -> List[Definition]:
        """Search for a word in the RAE dictionary"""
        try:
            word = word.strip().lower()
            url = f'{self.base_url}{word}'
            response = requests.get(
                url,
                headers=self.headers,
                timeout=10
            )
            response.raise_for_status()
            entry_response: WordEntryResponse = response.json()

            if entry_response.get('ok') == False:
                return []

            return self.get_word_senses(entry_response.get('data'), max_results)

        except requests.exceptions.RequestException as e:
            logger.error(f"Request error: {str(e)}")
            return []

        except Exception as e:
            logger.error(f"Unexpected error: {str(e)}")
            return []
    
    def get_word_senses(
            self, word_entry: WordEntry,
            max_results: int
    ) -> List[Definition]:
        return [x for x in word_entry.get('meanings')[0].get('senses')[:max_results]]
