from ulauncher.api.client.Extension import Extension
from ulauncher.api.client.EventListener import EventListener
from ulauncher.api.shared.event import KeywordQueryEvent 
from ulauncher.api.shared.item.ExtensionResultItem import ExtensionResultItem
from ulauncher.api.shared.action.RenderResultListAction import RenderResultListAction
from ulauncher.api.shared.action.CopyToClipboardAction import CopyToClipboardAction
from ulauncher.api.shared.action.HideWindowAction import HideWindowAction
from api_types import SearchStatus
from rae_api import RAEAPI

class RAEExtension(Extension):
    def __init__(self):
        super().__init__()
        self.rae_api = RAEAPI()
        self.subscribe(KeywordQueryEvent, KeywordQueryEventListener())


class KeywordQueryEventListener(EventListener):
    def on_event(self, event: KeywordQueryEvent, extension: RAEExtension):
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

        try:
            max_results = int(extension.preferences.get('max_results', 5))

            result = extension.rae_api.search_word(query, max_results)
            status = result.get('status')

            if status is SearchStatus.NETWORK_ERROR:
                return RenderResultListAction([
                    ExtensionResultItem(
                        icon='images/icon.png',
                        name=f'Can noy connect to RAE API',
                        description='Check your internet connection and try again',
                        on_enter=HideWindowAction()
                    )
                ])

            if status is SearchStatus.RATE_LIMIT:
                wait = f'{result.get('retry_after')} seconds'
                return RenderResultListAction([
                    ExtensionResultItem(
                        icon='images/icon.png',
                        name=f'RAE API rate limit exceeded',
                        description=f'Try again in {wait}',
                        on_enter=HideWindowAction()
                    )
                ])

            if status is SearchStatus.NOT_FOUND:
                suggestions = ', '.join(result.get('suggestions') or []) or ''
                return RenderResultListAction([
                    ExtensionResultItem(
                        icon='images/icon.png',
                        name=f'No definitions found for "{query}"',
                        description=f'Sug.: {suggestions}',
                        on_enter=HideWindowAction()
                    )
                ])

            if status is SearchStatus.API_ERROR:
                message = result.get('message', 'Unknown error')
                return RenderResultListAction([
                    ExtensionResultItem(
                        icon='images/icon.png',
                        name='Unexpected error',
                        description=f'{message}',
                        on_enter=HideWindowAction()
                    )
                ])

            items = []
            senses = result.get('data', [])
            for sense in senses:
                number = sense.get('meaning_number')
                description = sense.get('description')
                synonyms = ', '.join(sense.get('synonyms') or []) or ''
                category = sense.get('category')
                items.append(
                    ExtensionResultItem(
                        icon='images/icon.png',
                        name=f'{number}. {description}.',
                        description=f'Cat.: {category}. | Syn.: {synonyms}.',
                        on_enter=CopyToClipboardAction(description)
                    )
                )

            return RenderResultListAction(items)
        
        except Exception as e:
           return RenderResultListAction([
               ExtensionResultItem(
                   icon='images/icon.png',
                   name='Unexpected error',
                   description=f'{e}',
                   on_enter=HideWindowAction()
               )
           ])

if __name__ == '__main__':
    RAEExtension().run()
