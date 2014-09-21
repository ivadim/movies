import datetime, dateutil

import urllib, httplib, urlparse
import utils

class SimpleRestApiClient:
    """
    Create rest client for simplifying http/https requests
    """

    def __init__(self, base_url, common_url_params = {}):
        """
        * base_url - usually endpoint of rest api http://example/api/v2
        * common_url_params - url params which will be mixed into every request. For example api key
        """
        self.base_url = base_url
        self.common_url_params = common_url_params

    def GET(self, action_url, url_params = {}):
        """
        Make GET request
        """
        url = self.base_url + "/" + action_url
        parsed_url = urlparse.urlparse(url)
        if parsed_url.scheme == 'https':
            connection = httplib.HTTPSConnection(parsed_url.hostname)
        else:
            connection = httplib.HTTPConnection(parsed_url.hostname)
        get_path = parsed_url.path
        query = urllib.urlencode(utils.merge_dicts(self.common_url_params, url_params))
        if query:
            get_path += "?" + query
        connection.request('GET', get_path)
        response = connection.getresponse()
        response_data = response.read()
        connection.close()
        return response_data

    def POST(self, action_url, url_params=None, post_data=None):
        """
        Make GET request
        """
        raise Exception("Not implemented yet")


def merge_dicts(dict1, dict2):
    """
    Merge two dicts into 1
    """
    z = dict1.copy()
    z.update(dict2)
    return z

def calculate_age(born_str, today=None):
    """
    Calculate age by date of birth
    """
    if not born_str:
        return None
    if not today:
        today = datetime.date.today()
    born = dateutil.parser.parse(born_str)
    return today.year - born.year - ((today.month, today.day) < (born.month, born.day))

def calc_average(total_age, cast_number, none_number):
    """
    Calculate age average for film
    """
    average = 0
    if (cast_number - none_number) != 0:
        average = total_age / (cast_number - none_number)
    return float(average)

def calc_accuracy(cast_number, none_number):
    accuracy = 100*(cast_number - none_number)/cast_number
    return float(accuracy)
