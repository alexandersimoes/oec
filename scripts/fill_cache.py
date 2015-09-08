import click
import urllib2
import json
import time
import threading
from math import floor

from selenium import webdriver
from selenium.webdriver.common.by import By



def url_to_json(url):
    response = urllib2.urlopen(url)
    result = json.load(response)
    if 'data' in result:
        return result['data']
    raise Exception("No data!")

def crawl_attr(base_url, attr_kind='country'):
    driver = webdriver.Firefox()

    data = url_to_json('{}/attr/{}/'.format(base_url, attr_kind))
    data = sorted(data, key=lambda obj: obj['weight'] if 'weight' in obj else 0, reverse=True)
    for country in data:
        if 'display_id' in country:
            display_id = country['display_id']
            url_to_crawl = '{}/en/profile/{}/{}'.format(base_url, attr_kind, display_id)
            crawl_page(driver, url_to_crawl)

def crawl_page(driver, page):
    driver.get(page)

    driver.implicitly_wait(5)

    elems = driver.find_elements(By.XPATH, '//article/section/aside/h2')
    for elem in elems[: int(floor(len(elems) / 2))]:
        driver.execute_script('arguments[0].scrollIntoView(true);', elem);
        time.sleep(0.2)

@click.command()
@click.argument('base_url', type=str)
def main(base_url):
    if not base_url.startswith('http://'):
        base_url = 'http://' + base_url

    if base_url.endswith('/'):
        base_url = base_url[:-1]

    attrs = ['country', 'hs92']
    thread_list = []
    for attr in attrs:
        thread = threading.Thread(target=crawl_attr, args=[base_url, attr])
        thread.start()
        thread_list.append(thread)

    print "Waiting for crawl to complete..."

    for thread in thread_list:
        thread.join()

    print "Crawl complete!"

if __name__ == "__main__":
    main()
