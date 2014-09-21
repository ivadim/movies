import unittest
import os
from movies import tmdb
import httpretty
import base


class TestUtils(base.BaseRestTest):

   
    @httpretty.activate
    def test_tmdb_now_playing_one_page(self):
        httpretty.register_uri(httpretty.GET, "https://api.themoviedb.org/3/movie/now_playing",
                           body=self.load_fixture('fixtures/tmdb/now_playing_page1.json'),
                           content_type="application/json")

        api = tmdb.API(api_key='123')
        results = api.get_now_playing(start_page=1, max_pages=1)
        self.assertEqual(httpretty.last_request().querystring['api_key'], ['123'])
        self.assertEqual(httpretty.last_request().querystring['page'], ['1'])
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].id, 290553)
        self.assertEqual(results[0].title, "Start Options Exit")


    @httpretty.activate
    def test_tmdb_now_playing_multipage(self):
        httpretty.register_uri(httpretty.GET, "https://api.themoviedb.org/3/movie/now_playing",
                           responses=[
                               httpretty.Response(body=self.load_fixture('fixtures/tmdb/now_playing_page1.json'),
                                                  status=200),
                               httpretty.Response(body=self.load_fixture('fixtures/tmdb/now_playing_page2.json'), 
                                                  status=200),
                            ])



        api = tmdb.API(api_key='123')
        results = api.get_now_playing(start_page=1, max_pages=2)
        self.assertEqual(len(results), 2)
        self.assertEqual(results[0].title, "Start Options Exit")
        self.assertEqual(results[1].title, "Falcon Rising")


    @httpretty.activate
    def test_tmdb_now_playing_second_page(self):
        httpretty.register_uri(httpretty.GET, "https://api.themoviedb.org/3/movie/now_playing",
                           responses=[
                               httpretty.Response(body=self.load_fixture('fixtures/tmdb/now_playing_page2.json'), 
                                                  status=200),
                            ])



        api = tmdb.API(api_key='123')
        results = api.get_now_playing(start_page=2, max_pages=10)
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].title, "Falcon Rising")

    @httpretty.activate
    def test_tmdb_movie_credits(self):
        httpretty.register_uri(httpretty.GET, "https://api.themoviedb.org/3/movie/270938/credits",
                           responses=[
                               httpretty.Response(body=self.load_fixture('fixtures/tmdb/credits_270938.json'), 
                                                  status=200),
                            ])



        api = tmdb.API(api_key='123')
        cast, crew = api.get_movie_credits(270938)
        self.assertEqual(len(cast), 2)
        self.assertEqual(len(crew), 1)

        self.assertEqual(cast, [64856, 2203])
        self.assertEqual(crew, [5917])

    @httpretty.activate
    def test_tmdb_person_info_with_birthday(self):
        httpretty.register_uri(httpretty.GET, "https://api.themoviedb.org/3/person/64856",
                           responses=[
                               httpretty.Response(body=self.load_fixture('fixtures/tmdb/person_64856.json'), 
                                                  status=200),
                            ])



        api = tmdb.API(api_key='123')
        person = api.get_person_info(64856)
        self.assertEqual(person.name, 'Michael Jai White')
        self.assertEqual(person.birthday, '1967-11-10')

    @httpretty.activate
    def test_tmdb_person_info_withot_birthday(self):
        httpretty.register_uri(httpretty.GET, "https://api.themoviedb.org/3/person/2203",
                           responses=[
                               httpretty.Response(body=self.load_fixture('fixtures/tmdb/person_2203.json'), 
                                                  status=200),
                            ])



        api = tmdb.API()
        person = api.get_person_info(2203)
        self.assertEqual(person.name, 'Neal McDonough')
        self.assertEqual(person.birthday, None)
