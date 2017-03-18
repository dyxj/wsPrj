#!python3
"""
base_utils.py
Contains common functions
"""
import json
import os
from selenium import webdriver

# Generate Header
def gen_header(header_desc, total_length, type='print'):
    if type == 'print':
        print(header_desc.center(total_length, '-'))
    else:
        return header_desc.center(total_length, '-')


# Write JSON data to file
def write_json_to_file(data, path):
    with open(path, 'w') as outfile:
        json.dump(data, outfile, ensure_ascii=False, indent=2, sort_keys=True)


# Load JSON data from file
def load_json_from_file(path):
    with open(path, 'r') as infile:
        data = json.load(infile)
    return data

# Get browser for selenium
# Note: path for linux env
def get_browser(type='', visible='Y'):
    if type == 'chrome':
        # chrome_driver_path = r"/home/xj/Programs/chromedriver"
        # browser = webdriver.Chrome(chrome_driver_path)
        browser = webdriver.Chrome()
        if visible == 'N':
            browser.set_window_position(0, 0)
            browser.set_window_size(0, 0)
    else:
        phantomjs_path = r"/home/xj/Programs/phantomjs-2.1.1-linux-x86_64/bin/phantomjs"
        browser = webdriver.PhantomJS(executable_path=phantomjs_path, service_log_path=os.path.devnull)
    return browser
