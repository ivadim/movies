import unittest
import datetime
from movies import utils
import httpretty

class TestUtils(unittest.TestCase):


    @httpretty.activate
    def test_rest_client_http(self):
        httpretty.register_uri(httpretty.GET, "http://example/api/v1/person/123",
                           body='[{"test": "test"}]',
                           content_type="application/json")

        rest = utils.SimpleRestApiClient('http://example/api/v1')
        response = rest.GET('person/123')
        self.assertEqual(response, '[{"test": "test"}]')
        self.assertEqual(httpretty.last_request().querystring, {})

    @httpretty.activate
    def test_rest_client_https(self):
        httpretty.register_uri(httpretty.GET, "https://example/api/v1/person",
                           body='[{"test": "test"}]',
                           content_type="application/json")

        rest = utils.SimpleRestApiClient('https://example/api/v1', common_url_params={'api_key':'123'})
        response = rest.GET('person', url_params={'id':'321'})
        self.assertEqual(response, '[{"test": "test"}]')
        self.assertEqual(httpretty.last_request().querystring['api_key'], ['123'])
        self.assertEqual(httpretty.last_request().querystring['id'], ['321'])

    def test_calc_accuracy(self):
        accuracy = utils.calc_accuracy(10, 0)
        self.assertEqual(accuracy, 100.0)

        accuracy = utils.calc_accuracy(10, 10)
        self.assertEqual(accuracy, 0.0)

        accuracy = utils.calc_accuracy(10, 5)
        self.assertEqual(accuracy, 50.0)

        accuracy = utils.calc_accuracy(10, 10)
        self.assertEqual(accuracy, 0.0)


    def test_merge_dicts(self):
        dict1 = {'a': '1', 'b': '2'}
        dict2 = {'c': '3', 'd': '4'}
        expected = {'a': '1', 'b': '2', 'c': '3', 'd': '4'}
        actual = utils.merge_dicts(dict1, dict2)
        self.assertDictEqual(actual, expected)

    def test_merge_dicts_intersect(self):
        dict1 = {'a': '1', 'b': '2'}
        dict2 = {'a': '4', 'd': '4'}
        expected = {'a': '4', 'b': '2', 'd': '4'}
        actual = utils.merge_dicts(dict1, dict2)
        self.assertDictEqual(actual, expected)

    def test_calculate_age_none(self):
        age = utils.calculate_age(None)
        self.assertEqual(age, None)

    def test_calculate_age(self):
        today = datetime.date(2014, 05, 03)
        age = utils.calculate_age('1988-05-03', today)
        self.assertEqual(age, 26)

        today = datetime.date(2014, 05, 02)
        age = utils.calculate_age('1988-05-03', today)
        self.assertEqual(age, 25)

        today = datetime.date(2014, 05, 03)
        age = utils.calculate_age('2015-05-03', today)
        self.assertEqual(age, -1)

    def test_calculate_age_exception(self):
        self.assertRaises(ValueError, utils.calculate_age, 'bla-bla')

    def test_calc_average(self):
        average_age = utils.calc_average(100, 4, 0)
        self.assertEqual(average_age, 25)

        average_age = utils.calc_average(100, 3, 1)
        self.assertEqual(average_age, 50)

        average_age = utils.calc_average(0, 5, 5)
        self.assertEqual(average_age, 0)