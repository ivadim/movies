import json
from movies import utils

class API(object):
    """
    Create Freebase Rest Api Client
    """
    endpoint = 'https://www.googleapis.com/freebase/v1'
    api_key = 'AIzaSyBf2qAv7n5CtxQhQ5dpx-mtka17CFZTXdY'
    

    def __init__(self, endpoint=None, api_key=None):
        if not endpoint:
            endpoint = API.endpoint
        if not api_key:
            api_key = API.api_key
        self.rest = utils.SimpleRestApiClient(endpoint, 
                                            common_url_params={'key': api_key})


    def search(self, filter, limit=10):
        """
        The Freebase Search API provides access to Freebase data given a free text query. 
        The results of the query are ordered and have a numerical relevancy score.
        https://developers.google.com/freebase/v1/search-overview
        """
        data = json.loads(self.rest.GET('search', url_params={'filter': filter.encode('utf-8'), 'limit': limit}))
        return data['result']
        
    def mqlread(self, query):
        """
        The MQL Read API access to the Freebase database using the Metaweb query language (MQL).
        https://developers.google.com/freebase/v1/mql-overview
        """
        data = json.loads(self.rest.GET('mqlread', url_params={'query': query.encode('utf-8')}))
        return data['result']

