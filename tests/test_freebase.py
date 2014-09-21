import unittest
import os
from movies import freebase
import httpretty
import base


class TestUtils(base.BaseRestTest):

   
    @httpretty.activate
    def test_freebase_search(self):
        httpretty.register_uri(httpretty.GET, "https://www.googleapis.com/freebase/v1/search",
                           body=self.load_fixture('fixtures/freebase/search_Neal_McDonough.json'),
                           content_type="application/json")

        api = freebase.API(api_key='123')
        result = api.search(filter=u'(all type:/people/person name:"Neal McDonough" notable:actor)')
        self.assertEqual(httpretty.last_request().querystring['key'], ['123'])
        self.assertEqual(httpretty.last_request().querystring['filter'], [u'(all type:/people/person name:"Neal McDonough" notable:actor)'])
        self.assertEqual(result[0]['name'], 'Neal McDonough')
        self.assertEqual(result[0]['mid'], '/m/03w4sh')

    @httpretty.activate
    def test_freebase_mqlread(self):
        httpretty.register_uri(httpretty.GET, "https://www.googleapis.com/freebase/v1/mqlread",
                           body=self.load_fixture('fixtures/freebase/mqlread_Neal_McDonough.json'),
                           content_type="application/json")

        api = freebase.API(api_key='123')
        result = api.mqlread(query='{"type":"/people/person","mid":"/m/03w4sh","/people/person/date_of_birth":null}')
        self.assertEqual(result['/people/person/date_of_birth'], '1966-02-13')