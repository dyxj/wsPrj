#! python3
"""
videodata.py
Stores classes for video data
"""
import base_utils as bu


class VideoData:
    """ Basic form of video data """

    def __init__(self, type, title, link, quality, currentepisode, maxepisode):
        self.type = type
        self.title = title
        self.link = link
        self.quality = quality
        self.currentepisode = currentepisode
        self.maxepisode = maxepisode

    @property
    def link(self):
        return self._link

    @link.setter
    def link(self, value):
        if isinstance(value, str):
            self._link = value.rstrip("/")
        else:
            self._link = value

    def __str__(self):
        return "type: {}\ntitle: {}\nlink: {}\nquality: {}" \
               "\ncurrentepisode: {}\nmaxepisode: {}\n".format(self.type, self.title,
                                                               self._link,
                                                               self.quality,
                                                               self.currentepisode,
                                                               self.maxepisode)


def load_tracklist_data(path):
    """
    :param path: location of json file
    :return: {str userid, list VideoData}
    """
    tracklist_data = bu.load_json_from_file(path)
    tracklist_dict = {}
    for t in tracklist_data:
        tempUser = t.get("userid")
        # video data object
        temp_vid = VideoData(t.get("type"), "", t.get("link"), t.get("req_quality"),
                             t.get("curr_episode"), t.get("max_episode"))

        tracklist_dict.setdefault(tempUser, list()).append(temp_vid)

    return tracklist_dict
