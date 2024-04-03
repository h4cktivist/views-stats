import requests
from bs4 import BeautifulSoup
import services


HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/104.0.5112.79 Safari/537.36'
}


def parse_views_vk(post_url):
    try:
        html = requests.get(post_url, headers=HEADERS).text
        soup = BeautifulSoup(html, 'html.parser')
        views_div = soup.find('div', class_='like_views like_views--inActionPanel')
        for task in services.tasks_in_background:
            if task['link'] == post_url:
                task['views'] = int(views_div.get('title').split()[0])
                task['status'] = 'done'
    except:
        services.tasks_in_background[0]['status'] = 'failed'
