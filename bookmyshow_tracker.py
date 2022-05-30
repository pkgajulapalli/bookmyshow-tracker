import json
import sys
import time

from bs4 import BeautifulSoup
import requests

import pyttsx3


engine = pyttsx3.init()

sleep_time_in_secs = 60


def get_movie_url():
    # Update this url
    return 'https://in.bookmyshow.com/buytickets/pvr-soul-spirit-central-mall-bellandur/cinema-bang-CXBL-MT/20220603'


def get_headers():
    return {
        'Accept': '*/*',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/101.0.4951.64 Safari/537.36',
    }


def get_show_details():
    movie_url = get_movie_url()
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
                    return json.loads(json.loads(show_data_line.split('JSON.parse(')[1].split(');')[0]).replace("\'", ""))
    return {}


def track_tickets(movie_name):
    show_details_json = get_show_details()
    events = show_details_json.get('ShowDetails')[0].get('Event')
    for event in events:
        if str(event.get('EventTitle')).lower().__contains__(movie_name):
            engine.say('Found movie')
            engine.runAndWait()
            exit(0)
    print('Movie is not available yet. Will try again in %d secs' % sleep_time_in_secs)
    time.sleep(sleep_time_in_secs)
    track_tickets(movie_name)


if __name__ == '__main__':
    movie_name = sys.argv[1].lower()
    print('Looking for movie: ' + movie_name)
    track_tickets(movie_name)
