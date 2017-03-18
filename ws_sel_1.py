#! python3
"""
ws_sel_1.py
web scrapping 123 with selenium
"""
import videodata as vd
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from base_utils import get_browser
import traceback

# Global Video Dict
videodict = {}


def basescraper(t, url):
    """
    :param t: single record from tracklist json (modified if changes detected)
    :param url: url serves as key
    :return: status update message
    """
    # Check if this data has been parsed
    global videodict
    if url not in videodict.keys():
        vidobj = parseweb(url)
        videodict[url] = vidobj
    else:
        vidobj = videodict.get(url)

    msg = process_vid_data(t, vidobj)
    return msg


def __get_movieinfo(videoinfo):
    qualityinfo = videoinfo[1].text.split(':', 1)[1].strip()
    vdObj = vd.VideoData("movie", None, None, qualityinfo, None, None)
    return vdObj


def __get_seriesinfo(videoinfo):
    episodeinfo = videoinfo[0].text.split('/')
    current_episode = episodeinfo[0].split(':')[1].strip()
    max_episode = episodeinfo[1].split(' ')[0]
    qualityinfo = videoinfo[2].text.split(':', 1)[1].strip()
    vdObj = vd.VideoData("series", None, None, qualityinfo, current_episode, max_episode)
    return vdObj


def parseweb(url):
    # Get response from url
    url = url.rstrip("/")
    # Get webdriver browser
    browser = get_browser()
    browser.set_window_size(1280, 1024)
    browser.get(url)

    # Wait for page to load by checking element (10 sec)
    pgdtl = WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, ".page-detail"))
    )

    # Check video type
    vidtype = browser.find_element(By.CSS_SELECTOR, ".breadcrumb li + li a").text.strip().lower()
    videoinfo = pgdtl.find_elements_by_css_selector(".mvici-right p")
    vidtitle = pgdtl.find_element_by_css_selector(".mvic-desc h3").text

    if vidtype == "tv-series":
        # This is a series
        videodataobject = __get_seriesinfo(videoinfo)
        videodataobject.link = url
        videodataobject.title = vidtitle
    elif vidtype == "movies":
        # This is a movie
        videodataobject = __get_movieinfo(videoinfo)
        videodataobject.link = url
        videodataobject.title = vidtitle
    else:
        videodataobject = None

    return videodataobject


def process_vid_data(vid_json, vid_obj):
    """
    modify json data if any changes and return user message
    """
    vidtype = vid_obj.type
    if vidtype == 'movie':
        msg = "{} | Quality: {} | {}".format(vid_obj.title, vid_obj.quality, vid_obj.link)
        if vid_obj.quality.lower() == vid_json.get('req_quality').lower():
            vid_json['req_quality'] = vid_obj.quality
            return "!!!READY!!! " + msg
        else:
            return "...not ready... " + msg
    elif vidtype == 'series':
        msg = "{} | Episode: {}/{} | {}".format(vid_obj.title, vid_obj.currentepisode, vid_obj.maxepisode, vid_obj.link)
        if int(vid_obj.currentepisode) > int(vid_json.get('curr_episode')):
            vid_json['curr_episode'] = vid_obj.currentepisode
            return "!!!UPDATED!!! " + msg
        else:
            return "...no update... " + msg
