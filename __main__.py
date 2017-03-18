#!python3
"""
main script
Start of the program
"""
import sys
import os
import argparse
import base_utils as bu
import userdata
import ws_sel_1
import ws_selenium
import msgbuilder
from urllib.parse import urlparse


def main():
    try:
        parser = argparse.ArgumentParser()
        parser.add_argument('--path', type=str, default='./data',
                            help='Path of data folder, default : ./data')

        args = parser.parse_args()
        datafolderpath = args.path
        os.chdir(datafolderpath)  # change working directory to data folder
        # Init parameters
        headerlength = 80

        # Start of program
        bu.gen_header('Start of program', headerlength)
        print("Looking for data in :- {}".format(os.getcwd()))
        datafolderpath = os.getcwd()

        # Initialize Data dictionaries
        # For getting data from userdata.json, (not required if using DB)
        # key = userid , value = userdata class
        bu.gen_header('Loading user data', headerlength)
        userpath = os.path.join(datafolderpath, 'userdata.json')
        userdata_dict = userdata.load_user_data(userpath)

        # Get track list from json
        tracklist_json = get_tracklist(datafolderpath)

        # Process data with webscrapers
        bu.gen_header('Processing', headerlength)
        usr_msgobj_dict = runjoblist(tracklist_json)

        # Print message
        bu.gen_header('Messages Obtained', headerlength)
        print("\n\n")
        for msg_usrid, msgobj in usr_msgobj_dict.items():
            msg_usr_name = userdata_dict.get(msg_usrid).name
            bu.gen_header('{}'.format(msg_usr_name), headerlength)
            # Due to windows console limitation have to replace ’ with '
            print(msgobj.build_str().replace("’", "'"))

        # Update json file
        update_tracklist(tracklist_json, datafolderpath)

        bool_run = True
        while bool_run:
            main_input = input("""\nEnter q to exit\n""")
            if main_input == 'q':
                bool_run = False

        sys.exit()

    except Exception as e:
        print(e)


def get_tracklist(cwdir):
    """
    Gets tracklist from tracklist.json
    """
    jsonpath = os.path.join(cwdir, 'tracklist.json')
    tracklist_json = bu.load_json_from_file(jsonpath)
    return tracklist_json


def update_tracklist(tracklist_json, cwdir):
    """
    Gets tracklist from tracklist.json
    """
    jsonpath = os.path.join(cwdir, 'tracklist.json')
    bu.write_json_to_file(tracklist_json, jsonpath)


def runjoblist(tracklist_json):
    """
    Uses corresponding webscrapper to check if there are any matches in tracklist
    :param tracklist_json: list of desired trackers corresponding to user id
    :return: usermsgs: dict{str,list} of messages for each user in tracklist
    """
    # Output messages
    usermsgs = {}

    for t in tracklist_json:
        tlink = t.get('link').rstrip("/")
        msg = None
        parsed_uri = urlparse(tlink)
        domain = "{uri.scheme}://{uri.netloc}".format(uri=parsed_uri)
        if domain == "https://SOMEEXAMPLEWEBSITE":
            # msg = ws_sel_1.basescraper(t, tlink)
            # modify domain name first
            print("This domain name has been removed. Please modify tracklistjsoon and __main__.py")
        elif domain == "https://piay.iflix.com":
            msg = ws_selenium.basescraper(t, tlink)
        else:
            print("There are no appropriate web scrappers prepared")

        if msg != None:
            userid = t.get('userid')
            if userid not in usermsgs:
                usermsgs[userid] = msgbuilder.BaseMsg()
            usermsgs[userid].add_message(msg)

    return usermsgs


if __name__ == "__main__":
    main()
