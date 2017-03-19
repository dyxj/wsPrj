# wsPrj - Web Scraping Project #

### Purpose ##
Wanted to learn python, so I made a web scraper to test out some of the features of python. Some things were written in a certain way to allow me to test out the features offered by python.

**What it does? :** Unified webscrapper output. I wanted a quick way to go through all my frequently visited websites to see if there are any updates, rather than doing it manually. For now, these websites are mainly sites that provide video streaming but it can also be use for other sites.

### How to run? ###
* python wsPrj
* add -h :- to view help
* add --path=[path of data folder] :- to set path of data folder

#### Setup ####
* requires **tracklist.json** and **userdata.json**. Sample provided in data folder
* Modify location of chromedriver and phantomjs(uses phantomjs by default) get_browser in **base_utils.py**. Do note the difference between windows and linux  
* Requirement file is provided. pip install -r requirements.txt

### Key Scripts? ###
* **\_\_main\_\_.py**
    * Main body of code, gets user data and job list from tracklist.json
    * Determines which parser to use based on domain.
    * Prints out message output of parsers according to user
* **ws_selenium.py**
    * Webscrapper of choice, webscrappers not included in this project were all made base of this.
    * Uses selenium to parse iflix.
    * Check if movie is available.
    * Check if there are any updates for series.
* **ws_basic.py (Example script, not utilized)**
    * Example of a basic webscrapper that doesn't handle JS.
* **ws_qt.py (Example script, not utilized)**
    * Example of a webscrapper using PyQt. Handles js and wait for element to load. But can only run once as QApplication can only be initiated once. Code has to be rework to pass in the whole job list -> process it -> return all outputs and close.
    * requires installation of PyQt4.

### Output Sample: ###
    ---------------------------------anonymousName1---------------------------------
    ...no update... The Big Bang Theory - Season 10 | Episode: 18/22 | https://SOMEEXAMPLEWEBSITE
    !!!READY!!! Assassin's Creed | Quality: HD | https://SOMEEXAMPLEWEBSITE
    ...no update... Captain America: The First Avenger @ ---> https://piay.iflix.com/https://piay.iflix.com/movies/captain-america--the-first-avenger-7770
    ...no update... Mr. Robot | Season 2 | Episode 12 | Link : https://piay.iflix.com/tv/mr.-robot-4130  
      
    ---------------------------------anonymousName2---------------------------------
    ...no update... Black Sails - Season 4 | Episode: 7/10 | https://SOMEEXAMPLEWEBSITE
    !!!READY!!! Assassin's Creed | Quality: HD | https://SOMEEXAMPLEWEBSITE
    ...not ready... The Great Wall | Quality: CAM | https://SOMEEXAMPLEWEBSITE
    ...not ready... La La Land | Quality: SD | https://SOMEEXAMPLEWEBSITE
    ...no update... Captain America: The First Avenger @ ---> https://piay.iflix.com/https://piay.iflix.com/movies/captain-america--the-first-avenger-7770
    ...no update... Black Sails | Season 4 | Episode 7 | Link : https://piay.iflix.com/tv/black-sails-1824
    ...no update... Mr. Robot | Season 2 | Episode 12 | Link : https://piay.iflix.com/tv/mr.-robot-4130
    ...no update... nomovieexample not found

### MISC. ###  
* This project served as a tutorial for myself.  
* I may re-visit this to provide proper UI with
    * PyQt
    * Kivy(interesting cross platform)
    * web interface(way more familiar with this)  
* Probably should not have reinitialize and call quit for each action to improve performance.
* Multi-threading could also help the performance when number of actions increases.
* But for now it does the job. Moving on to checkout tensorflow.
