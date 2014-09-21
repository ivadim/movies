from movies import main
from StringIO import StringIO
import base
import httpretty, sys


class TestUtils(base.BaseRestTest):


    @httpretty.activate
    def test_main_without_freebase(self):
        main.actors_cache={}
        httpretty.register_uri(httpretty.GET, "https://api.themoviedb.org/3/movie/now_playing",
                           responses=[
                               httpretty.Response(body=self.load_fixture('fixtures/tmdb/now_playing_page1.json'),
                                                  status=200),
                               httpretty.Response(body=self.load_fixture('fixtures/tmdb/now_playing_page2.json'),
                                                  status=200),
                            ])

        httpretty.register_uri(httpretty.GET, "https://api.themoviedb.org/3/movie/270938/credits",
                           responses=[
                               httpretty.Response(body=self.load_fixture('fixtures/tmdb/credits_270938.json'),
                                                  status=200),
                            ])

        httpretty.register_uri(httpretty.GET, "https://api.themoviedb.org/3/movie/290553/credits",
                           responses=[
                               httpretty.Response(body=self.load_fixture('fixtures/tmdb/credits_290553.json'),
                                                  status=200),
                            ])

        httpretty.register_uri(httpretty.GET, "https://api.themoviedb.org/3/person/64856",
                           responses=[
                               httpretty.Response(body=self.load_fixture('fixtures/tmdb/person_64856.json'),
                                                  status=200),
                            ])

        httpretty.register_uri(httpretty.GET, "https://api.themoviedb.org/3/person/2203",
                           responses=[
                               httpretty.Response(body=self.load_fixture('fixtures/tmdb/person_2203.json'),
                                                  status=200),
                            ])


        saved_stdout = sys.stdout
        try:
            out = StringIO()
            sys.stdout = out
            freebase = False
            main.main(10, 10, freebase, 1, 1)
            output = out.getvalue().strip()
            self.assertTrue("'Start Options Exit' average age is 46.0 with accuracy 50.0%" in output)
        finally:
            sys.stdout = saved_stdout



    @httpretty.activate
    def test_main_with_freebase(self):
        main.actors_cache={}
        httpretty.register_uri(httpretty.GET, "https://api.themoviedb.org/3/movie/now_playing",
                           responses=[
                               httpretty.Response(body=self.load_fixture('fixtures/tmdb/now_playing_page1.json'),
                                                  status=200),
                               httpretty.Response(body=self.load_fixture('fixtures/tmdb/now_playing_page2.json'),
                                                  status=200),
                            ])

        httpretty.register_uri(httpretty.GET, "https://api.themoviedb.org/3/movie/270938/credits",
                           responses=[
                               httpretty.Response(body=self.load_fixture('fixtures/tmdb/credits_270938.json'),
                                                  status=200),
                            ])

        httpretty.register_uri(httpretty.GET, "https://api.themoviedb.org/3/movie/290553/credits",
                           responses=[
                               httpretty.Response(body=self.load_fixture('fixtures/tmdb/credits_290553.json'),
                                                  status=200),
                            ])

        httpretty.register_uri(httpretty.GET, "https://api.themoviedb.org/3/person/64856",
                           responses=[
                               httpretty.Response(body=self.load_fixture('fixtures/tmdb/person_64856.json'),
                                                  status=200),
                            ])

        httpretty.register_uri(httpretty.GET, "https://api.themoviedb.org/3/person/2203",
                           responses=[
                               httpretty.Response(body=self.load_fixture('fixtures/tmdb/person_2203.json'),
                                                  status=200),
                            ])

        httpretty.register_uri(httpretty.GET, "https://www.googleapis.com/freebase/v1/search",
                           body=self.load_fixture('fixtures/freebase/search_Neal_McDonough.json'),
                           content_type="application/json")

        httpretty.register_uri(httpretty.GET, "https://www.googleapis.com/freebase/v1/mqlread",
                           body=self.load_fixture('fixtures/freebase/mqlread_Neal_McDonough.json'),
                           content_type="application/json")


        saved_stdout = sys.stdout
        try:
            out = StringIO()
            sys.stdout = out
            freebase = True
            main.main(10, 10, freebase, 1, 2)
            output = out.getvalue().strip()
            self.assertTrue("'Start Options Exit' average age is 47.0 with accuracy 100.0%" in output)
            self.assertTrue("'Falcon Rising' average age is 47.0 with accuracy 100.0%" in output)
        finally:
            sys.stdout = saved_stdout


    @httpretty.activate
    def test_main_with_freebase_empty(self):
        main.actors_cache={}
        httpretty.register_uri(httpretty.GET, "https://api.themoviedb.org/3/movie/now_playing",
                           responses=[
                               httpretty.Response(body=self.load_fixture('fixtures/tmdb/now_playing_page1.json'),
                                                  status=200),
                               httpretty.Response(body=self.load_fixture('fixtures/tmdb/now_playing_page2.json'),
                                                  status=200),
                            ])

        httpretty.register_uri(httpretty.GET, "https://api.themoviedb.org/3/movie/270938/credits",
                           responses=[
                               httpretty.Response(body=self.load_fixture('fixtures/tmdb/credits_270938.json'),
                                                  status=200),
                            ])

        httpretty.register_uri(httpretty.GET, "https://api.themoviedb.org/3/movie/290553/credits",
                           responses=[
                               httpretty.Response(body=self.load_fixture('fixtures/tmdb/credits_290553.json'),
                                                  status=200),
                            ])

        httpretty.register_uri(httpretty.GET, "https://api.themoviedb.org/3/person/64856",
                           responses=[
                               httpretty.Response(body=self.load_fixture('fixtures/tmdb/person_64856.json'),
                                                  status=200),
                            ])

        httpretty.register_uri(httpretty.GET, "https://api.themoviedb.org/3/person/2203",
                           responses=[
                               httpretty.Response(body=self.load_fixture('fixtures/tmdb/person_2203.json'),
                                                  status=200),
                            ])

        httpretty.register_uri(httpretty.GET, "https://www.googleapis.com/freebase/v1/search",
                           body=self.load_fixture('fixtures/freebase/search_zero_results.json'),
                           content_type="application/json")


        saved_stdout = sys.stdout
        try:
            out = StringIO()
            sys.stdout = out
            freebase = True
            main.main(10, 10, freebase, 1, 2)
            output = out.getvalue().strip()
            self.assertTrue("'Start Options Exit' average age is 46.0 with accuracy 50.0%" in output)
            self.assertTrue("'Falcon Rising' average age is 46.0 with accuracy 50.0%" in output)
        finally:
            sys.stdout = saved_stdout



    @httpretty.activate
    def test_main_with_freebase_multi_results(self):
        main.actors_cache={}
        httpretty.register_uri(httpretty.GET, "https://api.themoviedb.org/3/movie/now_playing",
                           responses=[
                               httpretty.Response(body=self.load_fixture('fixtures/tmdb/now_playing_page1.json'),
                                                  status=200),
                               httpretty.Response(body=self.load_fixture('fixtures/tmdb/now_playing_page2.json'),
                                                  status=200),
                            ])

        httpretty.register_uri(httpretty.GET, "https://api.themoviedb.org/3/movie/270938/credits",
                           responses=[
                               httpretty.Response(body=self.load_fixture('fixtures/tmdb/credits_270938.json'),
                                                  status=200),
                            ])

        httpretty.register_uri(httpretty.GET, "https://api.themoviedb.org/3/movie/290553/credits",
                           responses=[
                               httpretty.Response(body=self.load_fixture('fixtures/tmdb/credits_290553.json'),
                                                  status=200),
                            ])

        httpretty.register_uri(httpretty.GET, "https://api.themoviedb.org/3/person/64856",
                           responses=[
                               httpretty.Response(body=self.load_fixture('fixtures/tmdb/person_64856.json'),
                                                  status=200),
                            ])

        httpretty.register_uri(httpretty.GET, "https://api.themoviedb.org/3/person/2203",
                           responses=[
                               httpretty.Response(body=self.load_fixture('fixtures/tmdb/person_2203.json'),
                                                  status=200),
                            ])

        httpretty.register_uri(httpretty.GET, "https://www.googleapis.com/freebase/v1/search",
                           body=self.load_fixture('fixtures/freebase/search_multy_results.json'),
                           content_type="application/json")


        saved_stdout = sys.stdout
        try:
            out = StringIO()
            sys.stdout = out
            freebase = True
            main.main(10, 10, freebase, 1, 2)
            output = out.getvalue().strip()
            self.assertTrue("'Start Options Exit' average age is 46.0 with accuracy 50.0%" in output)
            self.assertTrue("'Falcon Rising' average age is 46.0 with accuracy 50.0%" in output)
        finally:
            sys.stdout = saved_stdout



    @httpretty.activate
    def test_main_accuracy(self):
        main.actors_cache={}
        httpretty.register_uri(httpretty.GET, "https://api.themoviedb.org/3/movie/now_playing",
                           responses=[
                               httpretty.Response(body=self.load_fixture('fixtures/tmdb/now_playing_page1.json'),
                                                  status=200),
                               httpretty.Response(body=self.load_fixture('fixtures/tmdb/now_playing_page2.json'),
                                                  status=200),
                            ])

        httpretty.register_uri(httpretty.GET, "https://api.themoviedb.org/3/movie/270938/credits",
                           responses=[
                               httpretty.Response(body=self.load_fixture('fixtures/tmdb/credits_270938.json'),
                                                  status=200),
                            ])

        httpretty.register_uri(httpretty.GET, "https://api.themoviedb.org/3/movie/290553/credits",
                           responses=[
                               httpretty.Response(body=self.load_fixture('fixtures/tmdb/credits_290553.json'),
                                                  status=200),
                            ])

        httpretty.register_uri(httpretty.GET, "https://api.themoviedb.org/3/person/64856",
                           responses=[
                               httpretty.Response(body=self.load_fixture('fixtures/tmdb/person_64856.json'),
                                                  status=200),
                            ])

        httpretty.register_uri(httpretty.GET, "https://api.themoviedb.org/3/person/2203",
                           responses=[
                               httpretty.Response(body=self.load_fixture('fixtures/tmdb/person_2203.json'),
                                                  status=200),
                            ])


        saved_stdout = sys.stdout
        try:
            out = StringIO()
            sys.stdout = out
            freebase = False
            main.main(10, 51, freebase, 1, 2)
            output = out.getvalue().strip()
            self.assertTrue("'Start Options Exit' average age is 46.0 with accuracy 50.0%" not in output)
        finally:
            sys.stdout = saved_stdout


    @httpretty.activate
    def test_main_empty_cast(self):
        main.actors_cache={}
        httpretty.register_uri(httpretty.GET, "https://api.themoviedb.org/3/movie/now_playing",
                           responses=[
                               httpretty.Response(body=self.load_fixture('fixtures/tmdb/now_playing_empty.json'),
                                                  status=200)
                            ])

        httpretty.register_uri(httpretty.GET, "https://api.themoviedb.org/3/movie/111111/credits",
                           responses=[
                               httpretty.Response(body=self.load_fixture('fixtures/tmdb/credits_111111.json'),
                                                  status=200),
                            ])

        saved_stdout = sys.stdout
        try:
            out = StringIO()
            sys.stdout = out
            freebase = False
            main.main(10, 10, freebase, 1, 1)
            output = out.getvalue().strip()
            self.assertTrue("average age is" not in output)
        finally:
            sys.stdout = saved_stdout
