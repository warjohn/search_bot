from Bot.search.engine import SearchEngine
from Bot.search.config import PROXY, TIMEOUT, FAKE_USER_AGENT
from Bot.search.utils import unquote_url, quote_url


class SSMU(SearchEngine):
    '''Searches ssmu.ru'''

    def __init__(self, proxy=PROXY, timeout=TIMEOUT):
        super(SSMU, self).__init__(proxy, timeout)
        self._base_url = 'https://ssmu.ru'
        self._search_path = '/search/'
        self._delay = (2, 6)

        self.set_headers({'User-Agent': FAKE_USER_AGENT})

    def _first_page(self):
        '''Returns the initial page and query.'''
        # Получаем начальную страницу с запросом
        url = f'{self._base_url}{self._search_path}?q={quote_url(self._query, "")}'

        """        response = self._get_page(url)
        bs = BeautifulSoup(response.html, "html.parser")

        # Сбор всех input-полей формы
        inputs = {}
        for i in bs.select('form input[name]'):
            name = i.get('name')
            value = i.get('value', '')

            # Сохраняем все значения, кроме пустых полей
            if name and name != 'btnI':  # игнорируем кнопку submit
                if name in inputs:
                    # Если значение уже есть, добавляем к существующему
                    inputs[name].append(value)
                else:
                    # Создаем новый список значений для этого имени
                    inputs[name] = [value]

        # Сохраняем значение для поиска
        inputs['q'] = quote_url(self._query, '')

        # Сформируем URL с параметрами
        url = u'{}/search?{}'.format(self._base_url, '&'.join([k + '=' + (v or '') for k, v in inputs.items()]))
        print(url)"""
        return {'url': url, 'data': None}


    def _get_url(self, tag, item='href'):
        '''Returns the URL of search results item.'''
        selector = self._selectors('url')
        url = self._get_tag_item(tag.select_one(selector), item)
        return unquote_url(url)

    def _get_text(self, tag, item='text'):
        '''Returns the text of search results items.'''
        tag = tag.select_one(self._selectors('text'))
        return '\n'.join(list(tag.stripped_strings)) if tag else ''



