#! python3
"""
ws_selenium.py
webscraping dynamic pages example
"""
import urllib.parse as uparse
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from base_utils import get_browser

# Parsed Data
datadict = {}


def basescraper(t, url):
    """
    :param t: single record from tracklist json (modified if changes detected)
    :return: status update message
    """
    global datadict
    t_type = t.get('type')
    if t_type == "series":
        key = url
        if key not in datadict.keys():
            dataobj = parsewebSeries(key)
            datadict[key] = dataobj
        else:
            dataobj = datadict.get(key)
    elif t_type == "movie":
        key = t.get("title")
        if key not in datadict.keys():
            dataobj = parsewebMovies(key)
            datadict[key] = dataobj
        else:
            dataobj = datadict.get(key)
    else:
        return "invalid video type defined, please check track.json"

    msg = process_vid_data(t, dataobj)
    return msg


def parsewebSeries(url):
    try:
        browser = get_browser()
        browser.get(url)
        # Wait for page to load by checking element (10 sec)
        WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".season-header ul li a"))
        )
        # Parse page
        title = browser.find_element(By.CSS_SELECTOR, ".metainfo h1").get_attribute('innerHTML').strip()
        seasonEpisodeCount = browser.find_elements(By.CSS_SELECTOR, ".season-header ul li a i")

        # Click last season
        # seasonEpisodeCount[season-1].click()

        # Process page data
        totalEpisodeCount = 0
        for episodeCount in seasonEpisodeCount:
            tempCount = episodeCount.get_attribute('innerHTML').strip()
            tempCount = ''.join(filter(lambda x: x.isdigit(), tempCount))
            totalEpisodeCount += int(tempCount)

        season = len(seasonEpisodeCount)
        msgEpisode = tempCount
        tempmsg = "{} | Season {} | Episode {} | Link : {}".format(title, season, msgEpisode, url)
        dataobj = {'tempmsg': tempmsg, 'totalepisode': totalEpisodeCount}
        return dataobj

    except TimeoutException as e:
        print("TimeoutException")
        print(e)
    finally:
        browser.quit()


def parsewebMovies(title):
    try:
        modtitle = uparse.quote_plus(title)
        querylink = r"https://piay.iflix.com/search?query=" + modtitle
        browser = get_browser()
        browser.get(querylink)
        # Wait for page to load by checking element (10 sec)
        found = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".covers, .no-items raw strong"))
        )

        # Process page data
        if str(found.get_attribute("class").strip()) == 'covers':
            firstlink = browser.find_element(By.CSS_SELECTOR, ".cover").get_attribute('href')
            link = r"https://piay.iflix.com/" + firstlink
            tempmsg = "{} @ ---> {}".format(title, link)
            status = 1
        else:
            tempmsg = "{} not found".format(title)
            status = 0

        dataobj = {'tempmsg': tempmsg, 'status': status}
        return dataobj

    except TimeoutException as e:
        print("TimeoutException")
        print(e)
    finally:
        browser.quit()


def process_vid_data(vid_json, dataobj):
    """
    modify json data if any changes and return user message
    """
    vidtype = vid_json.get('type')
    if vidtype == 'movie':
        # tempmsg and status
        if vid_json['status'] != dataobj['status']:
            vid_json['status'] = dataobj['status']
            return "!!!UPDATED!!! " + dataobj['tempmsg']
        else:
            return "...no update... " + dataobj['tempmsg']
    elif vidtype == 'series':
        if int(dataobj['totalepisode']) > int(vid_json.get('curr_episode')):
            vid_json['curr_episode'] = dataobj['totalepisode']
            return "!!!UPDATED!!! " + dataobj['tempmsg']
        else:
            return "...no update... " + dataobj['tempmsg']


def test():
    # test
    try:
        title = "Captain America: The First Avenger"
        parsewebMovies(title)
        parsewebSeries("https://piay.iflix.com/tv/mr.-robot-4130")

    except Exception as e:
        print(e)


if __name__ == "__main__":
    test()
