[![Build Status](https://travis-ci.org/ivadim/movies.svg?branch=master)](https://travis-ci.org/ivadim/movies)
[![Coverage Status](https://img.shields.io/coveralls/ivadim/movies.svg)](https://coveralls.io/r/ivadim/movies?branch=master)

```
usage: python -m movies.main [-h] [-c CONCURRENCY] [-f] [-a ACCURACY] [-p MAX_PAGES]
               [-s START_PAGE]

optional arguments:
  -h, --help            show this help message and exit
  -c CONCURRENCY, --concurrency CONCURRENCY
                        number of parallel workers
  -f, --freebase        fallback to freebase to find actor's birthday
  -a ACCURACY, --accuracy ACCURACY
                        Min accuracy to show
  -p MAX_PAGES, --max_pages MAX_PAGES
                        Max number of pages from tmdb now playing api
  -s START_PAGE, --start_page START_PAGE
                        Start page from tmdb now playing api
                        
```
