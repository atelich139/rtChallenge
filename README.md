## Installing dependencies
`cd rtChallenge`

`pip install -r requirements.txt`

## Starting the webserver
`cd rtChallenge`

`python main.py`

Server will start at http://127.0.0.1:5000/

## Demo with cURL
`~ curl -d "url=https://www.lendingtree.com/reviews/personal/upgrade-inc/73349634" http://127.0.0.1:5000/reviews`

## To run tests

`pytest`


## Known issues
* This service isn't able to get all the reviews for each lender. For example; for the lender, First
  Midwest Bank, the service gets 2140 / 3146 reviews. I think this
is due to anti-scraping measures on lendingtree's end. I've tried the following approaches
  with no success: 
  1. changing the User-Agent header between each request
    2. sleeping between requests
    3. clearing cookies between requests
    4. mimicking the exact browser headers when you move to a new page from a previous page
    

* Possible solutions:
    1. using selenium as a headless browser to imitate a human user
    2. routing each request through a proxy server to act as though each one is coming from a different client
