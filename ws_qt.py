#! python3
"""
ws_qt.py
webscraping dynamic pages example
Can only run ones though, as QApplication can only be initiated once
so code has to be reworked to get all job list before
"""
import sys
from PyQt4.QtGui import QApplication
from PyQt4.QtCore import *
from PyQt4.QtWebKit import QWebPage
import bs4

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
    else:
        return "invalid video type defined, please check track.json"

    msg = process_vid_data(t, dataobj)
    return msg


def parsewebSeries(url):
    client_response = Client(url, ".season-header ul li a", True)
    source = client_response.mainFrame().toHtml()
    soup = bs4.BeautifulSoup(source, 'lxml')
    title = soup.select_one(".metainfo h1").get_text().strip()
    seasonEpisodeCount = soup.select(".season-header ul li a i")
    totalEpisodeCount = 0
    for episodeCount in seasonEpisodeCount:
        print(episodeCount)
        tempCount = ''.join(filter(lambda x: x.isdigit(), episodeCount.get_text()))
        totalEpisodeCount += int(tempCount)

    season = str(len(seasonEpisodeCount))
    msgEpisode = tempCount
    tempmsg = "{} | Season {} | Episode {} | Link : {}".format(title, season, msgEpisode, url)
    dataobj = {'tempmsg': tempmsg, 'totalepisode': totalEpisodeCount}
    return dataobj


class Client(QWebPage):
    def __init__(self, url, eoi, click):
        self.app = QApplication(sys.argv)
        QWebPage.__init__(self)
        qurl = QUrl(url)
        # element of interest & click bool
        self.eoi = eoi
        self.click = click
        self.mainFrame().load(qurl)
        self.on_webView_loadFinished()
        self.app.exec()

    @pyqtSlot()
    def on_webView_loadFinished(self):
        self.tObject = QTimer()
        self.tObject.setInterval(500)
        self.tObject.setSingleShot(True)
        self.tObject.timeout.connect(self.on_tObject_timeout)
        self.tObject.start()

    @pyqtSlot()
    def on_tObject_timeout(self):
        dElement = self.currentFrame().documentElement()
        elements = dElement.findAll(self.eoi)
        if elements.count() < 1:
            # Page not loaded
            # print("page not loaded")
            self.tObject.start()
        else:
            # Page loaded
            # print("page loaded")
            if (self.click == True):
                self.clickElement(elements)
            self.loadFinished.connect(self.on_page_load)

    # Clicks last element
    def clickElement(self, elements):
        totallen = len(elements)
        elements[totallen - 1].evaluateJavaScript(
            "var evObj = document.createEvent('MouseEvents');evObj.initEvent( 'click', true, true );this.dispatchEvent(evObj);")

    def on_page_load(self):
        self.app.quit()


def process_vid_data(vid_json, dataobj):
    """
    modify json data if any changes and return user message
    """
    print(vid_json.get('type'))
    vidtype = vid_json.get('type')
    if vidtype == 'series':
        if int(dataobj['totalepisode']) > int(vid_json.get('curr_episode')):
            vid_json['curr_episode'] = dataobj['totalepisode']
            return "!!!UPDATED!!!" + dataobj['tempmsg']
        else:
            return "...no update..." + dataobj['tempmsg']


def main():
    try:
        parsewebSeries("https://piay.iflix.com/tv/mr.-robot-4130")

    except Exception as e:
        print(e)


if __name__ == "__main__":
    main()
