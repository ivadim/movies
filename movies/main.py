#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pprint import pprint
import timeit, datetime, argparse
from movies import worker, tmdb, freebase, utils

tmdb_api = tmdb.API()
freebase_api = freebase.API()

actors_cache = {}


def try_find_birthday_in_freebase(name):
    search_result = freebase_api.search(filter=u'(all type:/people/person name:"%s" notable:actor)'  % name )
    if len(search_result) == 0 or len(search_result) > 1:
        return None # there is no results or more then 1. Can't understand what to do
    mid = search_result[0]['mid']
    person = freebase_api.mqlread(query='{"type":"/people/person","mid":"%s","/people/person/date_of_birth":null}' % mid)
    return person['/people/person/date_of_birth']


def process_movie(movie, min_accuracy, use_freebase):
    cast, crew = tmdb_api.get_movie_credits(movie.id)
    none_number = 0;
    total_age = 0;
    if len(cast) == 0:
        #Didn't find any actors in film
        return
    for person_id in cast:
        if person_id in actors_cache:
            person = actors_cache[person_id]
        else:
            person = tmdb_api.get_person_info(person_id)
            if not person.birthday and use_freebase:
                person.birthday = try_find_birthday_in_freebase(person.name)
            actors_cache[person_id] = person
        if not person.birthday:
            none_number += 1;
        else:
            total_age += utils.calculate_age(person.birthday)
    accuracy = utils.calc_accuracy(len(cast), none_number) 
    average = utils.calc_average(total_age, len(cast), none_number)
    if accuracy >= min_accuracy:
        print "'{}' average age is {:.4} with accuracy {:.4}%".format(movie.title.encode('utf-8'), average, accuracy)


def main(concurrency, accuracy, freebase, start_page, max_pages):
    
    start = timeit.default_timer()
    
    thread_pool = worker.ThreadPool(concurrency)

    for movie in tmdb_api.get_now_playing(start_page=start_page, max_pages=max_pages):
        thread_pool.add_task(process_movie, movie, accuracy, freebase)

    thread_pool.wait_completion()

    end = timeit.default_timer()
    spent = (end - start)
    formated_time = datetime.timedelta(seconds=spent)
    
    print "Total time: {}".format(formated_time)



if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--concurrency", help="number of parallel workers", default=25, type=int, required=False)
    parser.add_argument("-f", "--freebase", help="fallback to freebase to find actor's birthday", action='store_true', default=False)
    parser.add_argument("-a", "--accuracy", help="Min accuracy to show", default=70, type=int)
    parser.add_argument("-p", "--max_pages", help="Max number of pages from tmdb now playing api", default=3, type=int)
    parser.add_argument("-s", "--start_page", help="Start page from tmdb now playing api", default=1, type=int)

    args = parser.parse_args()
    main(args.concurrency, args.accuracy, args.freebase, args.start_page, args.max_pages)
