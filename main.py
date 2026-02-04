import logging
from ulauncher.api.client.Extension import Extension
from ulauncher.api.client.EventListener import EventListener
from ulauncher.api.shared.event import KeywordQueryEvent 
from ulauncher.api.shared.item.ExtensionResultItem import ExtensionResultItem
from ulauncher.api.shared.item.SmallResultItem import SmallResultItem
from ulauncher.api.shared.action.RenderResultListAction import RenderResultListAction
from ulauncher.api.shared.action.CopyToClipboardAction import CopyToClipboardAction
from ulauncher.api.shared.action.HideWindowAction import HideWindowAction
from rae_api import RAEAPI

logger = logging.getLogger(__name__)

class RAEExtension(Extension):
    def __init__(self):
        super().__init__()
        self.rae_api = RAEAPI()
        self.subscribe(KeywordQueryEvent, KeywordQueryEventListener())


class KeywordQueryEventListener(EventListener):
    def on_event(self, event, extension):
        query = event.get_argument()

        if not query or len(query.strip()) < 2:
            return RenderResultListAction([
                ExtensionResultItem(
                    icon='images/icon.png',
                    name='Type a word to search (min. 2 characters)',
                    description='Example: "casa", "amor", "computadora"',
                    on_enter=HideWindowAction()
                )
            ])

        max_results = int(extension.preferences.get('max_results', 5))
        senses = extension.rae_api.search_word(query, max_results)

        items = []
        for sense in senses:
            number = sense.get('meaning_number')
            description = sense.get('description')
            synonyms = ', '.join(sense.get('synonyms', []))
            category = sense.get('category')
            items.append(
                ExtensionResultItem(
                    icon='images/icon.png',
                    name=f'{number}: {description}.',
                    description=f'Cat.: {category}. | Syn.: {synonyms}.',
                    on_enter=CopyToClipboardAction(description)
                )
            )

        return RenderResultListAction(items)

if __name__ == '__main__':
    RAEExtension().run()
