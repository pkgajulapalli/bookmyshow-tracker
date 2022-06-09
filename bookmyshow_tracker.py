import argparse
import json
import logging
import time

from bs4 import BeautifulSoup
import requests

import pyttsx3

from email_utility import send_email

engine = pyttsx3.init()
logging.root.setLevel(logging.INFO)
logging.basicConfig(
    format='%(asctime)s.%(msecs)03d %(levelname)s %(module)s - %(funcName)s: %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S')

parser = argparse.ArgumentParser(description='Track for ticket availability in BookMyShow.')
parser.add_argument('-s', '--sleep_time_in_secs', dest='sleep_time_in_secs', type=int, default=60,
                    help='sleep time between retries in seconds')
parser.add_argument('-e', '--email_id', dest='email_id', type=str, default=None,
                    help='Email to deliver the notification')
requiredNamed = parser.add_argument_group('required named arguments')
requiredNamed.add_argument('-m', '--movie_name', dest='movie_name', type=str, help='Name of the movie to search for',
                           required=True)
requiredNamed.add_argument('-u', '--url', dest='movie_url', type=str, required=True,
                           help='URL of the movie theater for the required date. '
                                'Eg: https://in.bookmyshow.com/bengaluru/cinemas/pvr-forum-mall-4dx-koramangala/PFKM/'
                                '20220531',)
requiredNamed.add_argument('-c', '--max_connection_timeouts', dest='max_connection_timeouts', type=int, default=10,
                           help='Maximum number of connection timeouts before failing')


def get_headers():
    return {
        'Accept': '*/*',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/101.0.4951.64 Safari/537.36',
    }


def get_show_details():
    response = requests.request('GET', movie_url, headers=get_headers(), data={})
    assert response.status_code == 200
    page_content = BeautifulSoup(response.content, features='lxml')
    script_elements = page_content.find_all('script')
    for script_element in script_elements:
        if script_element.text.__contains__('ShowDetails'):
            show_details_text = script_element.text
            for line in show_details_text.splitlines():
                if line.__contains__('var UAPI'):
                    show_data_line = line
                    return json.loads(json.loads(show_data_line.split('JSON.parse(')[1].split(');')[0]).
                                      replace("\'", ""))
    return {}


def say(text):
    engine.say(text)
    engine.runAndWait()
    if email_id is not None:
        send_email(email_id, 'Found movie', '<html><body><h1>%s</h1><a href="%s">Check here</a></body></html>' %
                   (text, movie_url))


# noinspection PyShadowingNames
def track_tickets(movie_name, connection_timeouts=0):
    try:
        show_details_json = get_show_details()
        events = show_details_json.get('ShowDetails')[0].get('Event')
        for event in events:
            movie = str(event.get('EventTitle'))
            if movie.lower().__contains__(movie_name):
                say('Found movie: ' + movie)
                exit(0)
        logging.info('Movie is not available yet. Will try again in %d secs' % sleep_time_in_secs)
        time.sleep(sleep_time_in_secs)
        track_tickets(movie_name)
    except requests.exceptions.ConnectionError as e:
        logging.error(e)
        if connection_timeouts >= max_connection_timeouts:
            say('Not able to connect to BookMyShow')
            exit(1)
        time.sleep(sleep_time_in_secs)
        track_tickets(movie_name, connection_timeouts + 1)


if __name__ == '__main__':
    args = parser.parse_args()
    movie_name = args.movie_name.lower()
    movie_url = args.movie_url
    email_id = args.email_id
    sleep_time_in_secs = args.sleep_time_in_secs
    max_connection_timeouts = args.max_connection_timeouts
    logging.info('Looking for movie: ' + movie_name)
    track_tickets(movie_name)
