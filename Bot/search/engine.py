from bs4 import BeautifulSoup
from time import sleep
from random import uniform as random_uniform
from collections import namedtuple

from Bot.search.results import SearchResults
from Bot.search.http_client import HttpClient
import Bot.search.utils as utils
import Bot.search.output as out
import Bot.search.config as cfg
from tqdm import tqdm


class SearchEngine(object):
    '''The base class for all Search Engines.'''

    def __init__(self, proxy=cfg.PROXY, timeout=cfg.TIMEOUT):
        '''
        :param str proxy: optional, a proxy server
        :param int timeout: optional, the HTTP timeout
        '''
        self._http_client = HttpClient(timeout, proxy)
        self._delay = (1, 4)
        self._query = ''
        self._filters = []

        self.results = SearchResults()
        '''The search results.'''
        self.ignore_duplicate_urls = False
        '''Collects only unique URLs.'''
        self.ignore_duplicate_domains = False
        '''Collects only unique domains.'''
        self.is_banned = False
        '''Indicates if a ban occured'''

    def _selectors(self, element):
        '''Returns the appropriate CSS selector.'''
        raise NotImplementedError()

    def _first_page(self):
        '''Returns the initial page URL.'''
        raise NotImplementedError()

    def _next_page(self, tags):
        '''Returns the next page URL and post data (if any)'''
        # tags = self._check_consent(tags)

        next_button = tags.select_one('a.btn.search-page__more._bordered._secondary')
        if next_button is not None:
            link = next_button.get('href')
            next_url = link if next_button else None
            url = None
            if next_url:
                url = self._base_url + next_url
            return {'url': url, 'data': None}
        else:
            return None

    def _get_url(self, tag, item='href'):
        '''Returns the URL of search results items.'''
        selector = self._selectors('url')
        url = self._get_tag_item(tag.select_one(selector), item)
        return utils.unquote_url(url)

    def _get_title(self, tag, item='text'):
        '''Returns the title of search results items.'''
        selector = self._selectors('title')
        return self._get_tag_item(tag.select_one(selector), item)

    def _get_text(self, tag, item='text'):
        '''Returns the text of search results items.'''
        selector = self._selectors('text')
        return self._get_tag_item(tag.select_one(selector), item)

    def _get_page(self, page, data=None):
        '''Gets pagination links.'''
        if data:
            return self._http_client.post(page, data)
        return self._http_client.get(page)

    def _get_tag_item(self, tag, item):
        '''Returns Tag attributes.'''
        if not tag:
            return u''
        return tag.text if item == 'text' else tag.get(item, u'')

    def _item(self, link):
        '''Returns a dictionary of the link data.'''
        return {
            'host': utils.domain(self._get_url(link)),
            'link': self._get_url(link),
            'title': self._get_title(link).strip(),
            'text': self._get_text(link).strip()
        }

    def _query_in(self, item):
        '''Checks if query is contained in the item.'''
        return self._query.lower() in item.lower()

    def _filter_results(self, soup):
        '''Processes and filters the search results.'''
        articles = soup.select('article.search-page__item')
        results = []
        for article in articles:
            link_tag = article.select_one('a')
            text_tag = article.select_one('p')

            if link_tag and text_tag:
                link = link_tag.get('href')

                title = link_tag.get_text(strip=False)

                text = text_tag.get_text(strip=False)


                item = {
                    'link': self._base_url + link,
                    'title': title,
                    'text': text
                }
                results.append(item)

        # Apply filters
        if 'url' in self._filters:
            results = [l for l in results if self._query_in(l['link'])]
        if 'title' in self._filters:
            results = [l for l in results if self._query_in(l['title'])]
        if 'text' in self._filters:
            results = [l for l in results if self._query_in(l['text'])]
        # if 'host' in self._filters:
        # results = [l for l in results if self._query_in(utils.domain(l['link']))]

        return results

    def _collect_results(self, items):
        '''Collects the search results items.'''
        for item in items:
            # Проверяем, является ли ссылка валидным URL
            if not utils.is_url(item['link']):
                continue
            # Проверяем, существует ли элемент уже в результатах
            if item in self.results:
                continue
            # Проверяем на дублирование URL, если включена соответствующая опция
            if self.ignore_duplicate_urls and item['link'] in self.results.links():
                continue
            # Проверяем на дублирование доменов, если включена соответствующая опция
            if self.ignore_duplicate_domains and utils.domain(item['link']) in self.results.hosts():
                continue

            # Добавляем элемент в результаты
            self.results.append(item)
        print("self.results", self.results)

    def _is_ok(self, response):
        '''Checks if the HTTP response is 200 OK.'''
        self.is_banned = response.http in [403, 429, 503]

        if response.http == 200:
            return True
        msg = ('HTTP ' + str(response.http)) if response.http else response.html
        out.console(msg, level=out.Level.error)
        return False

    def disable_console(self):
        '''Disables console output'''
        out.console = lambda msg, end='\n', level=None: None

    def set_headers(self, headers):
        '''Sets HTTP headers.

        :param headers: dict The headers
        '''
        self._http_client.session.headers.update(headers)

    def set_search_operator(self, operator):
        '''Filters search results based on the operator.
        Supported operators: 'url', 'title', 'text', 'host'

        :param operator: str The search operator(s)
        '''
        operators = utils.decode_bytes(operator or u'').lower().split(u',')
        supported_operators = [u'url', u'title', u'text', u'host']

        for operator in operators:
            if operator not in supported_operators:
                msg = u'Ignoring unsupported operator "{}"'.format(operator)
                out.console(msg, level=out.Level.warning)
            else:
                self._filters += [operator]

    def search(self, query, pages=cfg.SEARCH_ENGINE_RESULTS_PAGES):
        '''Queries the search engine, goes through the pages and collects the results.

        :param query: str The search query
        :param pages: int Optional, the maximum number of results pages to search
        :returns SearchResults object
        '''
        out.console('Searching {}'.format(self.__class__.__name__))
        self._query = utils.decode_bytes(query)
        self.results = SearchResults()
        request = self._first_page()
        print("request", request)
        for page in tqdm(range(1, pages + 1), desc="searching"):
            try:
                response = self._get_page(request['url'], request['data'])
                if not self._is_ok(response):
                    print("Error")
                    break
                tags = BeautifulSoup(response.html, "html.parser")

                items = self._filter_results(tags)

                request = self._next_page(tags)

                if request is None:
                    break
                if page < pages:
                    sleep(random_uniform(*self._delay))
            except KeyboardInterrupt:
                break
        out.console('', end='')
        return items

    def output(self, output=out.PRINT, path=None):
        '''Prints search results and/or creates report files.
        Supported output format: html, csv, json.

        :param output: str Optional, the output format
        :param path: str Optional, the file to save the report
        '''
        output = (output or '').lower()
        if not path:
            path = cfg.os_path.join(cfg.OUTPUT_DIR, u'_'.join(self._query.split()))
        out.console('')

        if out.PRINT in output:
            out.print_results([self])
        if out.HTML in output:
            out.write_file(out.create_html_data([self]), path + u'.html')
        if out.CSV in output:
            out.write_file(out.create_csv_data([self]), path + u'.csv')
        if out.JSON in output:
            out.write_file(out.create_json_data([self]), path + u'.json')
