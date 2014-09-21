import json
from movies import utils

class Person(object):

    def __init__(self, person_info):
        self.id = person_info['id']
        self.name = person_info['name']
        self.birthday = person_info['birthday']



class NowPlaying(object):

    def __init__(self, now_playing_info):
        data = json.loads(now_playing_info)
        self.page = data['page']
        self.total_pages = data['total_pages']
        self.total_results = data['total_results']
        self.dates = data['dates']
        self.results = []
        for item in data['results']:
            self.results.append(NowPlayingResultItem(item))

    def append_results(self, result_item_list):
        for item in result_item_list:
            self.results.append(item)

class NowPlayingResultItem(object):

    def __init__(self, data):
        self.id = data['id']
        self.original_title = data['original_title']
        self.title = data['title']
        self.release_date = data['release_date']


class API(object):
    """
    Create themoviedb.org Rest Api Client
    """
    endpoint = 'https://api.themoviedb.org/3'
    api_key = 'fa22629200936e5550c1ed576361ce6a'
    

    def __init__(self, endpoint=None, api_key=None):
        if not endpoint:
            endpoint = API.endpoint
        if not api_key:
            api_key = API.api_key
        self.rest = utils.SimpleRestApiClient(endpoint, 
                                            common_url_params={'api_key':api_key})


    def get_now_playing(self, max_pages=10, start_page=1):
        """
        Get current movies in theaters
        http://docs.themoviedb.apiary.io/reference/movies/movienowplaying/get
        Return list of NowPlayingResultItem objects
        """
        now_playing = NowPlaying(self.rest.GET('movie/now_playing', url_params={'page': start_page}))
        page = start_page + 1
        while (page <= now_playing.total_pages) and (page <= max_pages):
            new_page = NowPlaying(self.rest.GET('movie/now_playing', url_params={'page': page}))
            now_playing.append_results(new_page.results)
            page += 1
        
        return now_playing.results


    def get_movie_credits(self, id):
        """
        Get information about cast and crew in movie by id
        http://docs.themoviedb.apiary.io/reference/movies/movieidcredits/get
        Return turple of cast and crew lists of id
        """
        movie_credits = json.loads(self.rest.GET('movie/%s/credits' % id))
        cast = []
        crew = []
        for person in movie_credits['cast']:
            cast.append(person['id']) 
        for person in movie_credits['crew']:
            crew.append(person['id'])

        return (cast, crew)

    def get_person_info(self, id):
        """
        Get information about person
        http://docs.themoviedb.apiary.io/reference/people
        """
        info = json.loads(self.rest.GET('person/%s' % id))
        return Person(info)
