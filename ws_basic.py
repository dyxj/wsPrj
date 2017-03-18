#! python3
"""
ws_basic.py
webscraping basic example
"""
import requests
import bs4
import videodata as vd
import sys

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
    qualityinfo = videoinfo[1].get_text().split(':', 1)[1].strip()
    vdObj = vd.VideoData("movie", None, None, qualityinfo, None, None)
    return vdObj


def __get_seriesinfo(videoinfo):
    episodeinfo = videoinfo[0].get_text().split('/')
    current_episode = episodeinfo[0].split(':')[1].strip()
    max_episode = episodeinfo[1].split(' ')[0]
    qualityinfo = videoinfo[2].get_text().split(':', 1)[1].strip()
    vdObj = vd.VideoData("series", None, None, qualityinfo, current_episode, max_episode)
    return vdObj


def parseweb(url):
    # Get response from url
    url = url.rstrip("/")
    res = requests.get(url)

    try:
        # Check response status
        res.raise_for_status()
        # Parse response
        soup = bs4.BeautifulSoup(res.text, 'lxml')
        # Narrow down search to page details
        pgdtl = soup.select_one(".page-detail")

        # Check video_type
        vidtype = pgdtl.select_one(".breadcrumb li + li a").get_text().strip().lower()
        videoinfo = pgdtl.select(".mvici-right p")
        vidtitle = pgdtl.select_one(".mvic-desc h3").get_text()

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

    except Exception as ex:
        print(ex)


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
