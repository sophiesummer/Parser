from bs4 import BeautifulSoup
import urllib.request
import json
import re
import logging


start_url = "https://en.wikipedia.org/wiki/Morgan_Freeman"
pre_url = "https://en.wikipedia.org"
present_year = 2018


def make_soup(url):
    pages = urllib.request.urlopen(url)
    soup_data = BeautifulSoup(pages, "html.parser")
    return soup_data


class Scraper:
    def __init__(self, start_url, max_actor_num):
        self.actors_set = {}  # name : url
        self.movies_set = {}
        self.max_actor_num = max_actor_num
        self.max_movie_num = max_actor_num * 2
        self.curr_actor_num = 0
        self.curr_movie_num = 0
        self.actors_queue = []  # actor_name
        self.movies_queue = []  # movie_name
        self.start_url = start_url
        self.actors_data = []  # save result
        self.movies_data = []
        logging.basicConfig(filename='scraper_status.log', level=logging.DEBUG)

    def scrap_actor(self, actor_url, actor_name):
        logging.info("^^^^^^^^^^^")
        logging.info(actor_url)
        actor = dict()
        actor['movies'] = []
        actor['name'] = actor_name
        movie_list = {}
        actor['birthday'] = ''
        actor['age'] = -1

        try:
            logging.info('before actor soup')
            soup = make_soup(actor_url)
            logging.info('after actor soup')
            try:
                born_info = soup.find('table', {"class": re.compile('infobox.*')}).\
                    find('tbody').find('th', text=('Born')).find_parent('tr').\
                    find('span', {'class': "bday"}).text

            except:
                logging.debug('no birthday info')

            else:
                actor['birthday'] = born_info
                actor['age'] = present_year - int(born_info[:4])

            try:
                # if filmography is an outside page
                film_list = soup.find('div', {'id': 'mw-content-text'}). \
                    find('div', {'class': 'mw-parser-output'}). \
                    find_all("div", {"role": "note"})

                new_page = ""
                for f in film_list:
                    if "Main article" in f.text:
                        href = f.find('a')
                        new_page = href.get('href')
                        break

                if len(new_page) > 5:
                    new_page = pre_url + new_page
                    film_page_body = make_soup(new_page).find("div", {"class": "mw-parser-output"})
                    film_table = film_page_body.find("table", {'class': re.compile('.*wikitable.*')}).\
                        find("tbody")

                    for tr in film_table.find_all('tr'):
                        try:
                            each_film = tr.find("a")
                            if each_film:
                                film_web = each_film.get('href')  # without prehref
                                film_web = pre_url + film_web
                                film_name = each_film.text
                                if film_name[0] == '[' and film_name[-1] == ']':
                                    continue
                                actor['movies'].append(film_name)
                                movie_list[film_name] = film_web
                        except:
                            logging.debug('none href for current web')

            except:
                # if filmography is inside the webpage
                try:
                    film_table = soup.find('table', {'class': re.compile('.*wikitable.*')}).\
                        find('tbody').find_all('tr')
                    for tr in film_table:
                        each_film = tr.find("a")
                        if each_film:
                            film_web = each_film.get('href')  # without prehref
                            film_web = pre_url + film_web
                            film_name = each_film.text
                            if film_name[0] == '[' and film_name[-1] == ']':
                                continue
                            actor['movies'].append(film_name)
                            movie_list[film_name] = film_web
                except:
                    logging.warning("nothing in filmography")
            logging.info("^^^^^^^^^^^^^^^^^^^^")
            return actor, movie_list
        except:
            logging.warning('cannot make soup for this actor_link')
            return actor, movie_list


    def scrap_movie(self, movie_url, movie_name):
        movie = dict()
        movie['name'] = movie_name
        actor_list = {}
        movie['actors'] = []
        movie['gross'] = -1
        movie['year'] = -1

        try:
            logging.info('before movie soup')
            soup = make_soup(movie_url)
            logging.info('after movie soup')
            movie_info = soup.find('table', {"class": re.compile("infobox.*")}).find('tbody')

        except:
            logging.warning("no infobox in this movie page")
            return movie, actor_list

        else:
            try:
                box_office_title = movie_info.find('th', text=("Box office"))
                box_office = box_office_title.find_parent('tr').find('td').contents[0]
                movie['gross'] = self.box_office_format(box_office) # change to number function
            except:
                logging.warning("no gross info")

            try:
                release_date = movie_info.find('th', text=("Release date")).find_parent('tr').\
                    find('span', {'class': 'bday dtstart published updated'}).text
                movie['year'] = int(release_date[:4])
            except:
                try:
                    release_date = (movie_info.find('th', text=("Release date")).find_parent('tr').\
                        find('td').text)
                    movie['year'] = release_date[-4:]
                    movie['year'] = int(movie['year'])
                except:
                    logging.warning("no release year")

            try:
                star_list = movie_info.find('th', text=('Starring')).find_parent('tr').find_all('a')
                for a in star_list:
                    actor_name = a.text
                    try:
                        actor_link = a.get('href')
                        actor_link = pre_url + actor_link
                        actor_list[actor_name] = actor_link
                        movie['actors'].append(actor_name)
                    except:
                        logging.warning("no this star href")
            except:
                logging.warning('no starring info')

        return movie, actor_list

    def box_office_format(self, box_office):
        start = box_office.index("$")
        box_office = box_office[start + 1:]
        box_office = box_office.replace(',', '')

        gross = -1
        if "million" in box_office:
            end = box_office.index('million')
            box_office = box_office[:end - 1]
            gross = float(box_office) * 10**6
        elif "billion" in box_office:
            end = box_office.index('billion')
            box_office = box_office[:end - 1]
            gross = float(box_office) * 10**9
        elif " " in box_office:
            end = box_office.index(' ')
            box_office = box_office[:end]
            gross = float(box_office)
        else:
            gross = float(box_office)

        return gross

    def start_scrap(self):
        self.actors_set["Morgan Freeman"] = self.start_url
        self.actors_queue.append("Morgan Freeman")
        while self.curr_actor_num < self.max_actor_num or \
                self.curr_movie_num < self.max_movie_num:

            # scrape actors info
            while len(self.actors_queue) > 0 and self.curr_actor_num <= self.max_actor_num:
                logging.info("&&&&&& current : actor numbers: ")
                logging.info(self.curr_actor_num)
                actor_name = self.actors_queue[0]
                actor_url = self.actors_set[actor_name]
                self.actors_queue.pop(0)
                if len(actor_url) < 5:
                    continue

                actor, movie_list = self.scrap_actor(actor_url, actor_name)
                if (actor['birthday'] == "") and len(movie_list) == 0:
                    logging.debug('birthday and movie_list not exist')
                    continue

                self.actors_data.append(actor)
                self.curr_actor_num += 1
                for movie_name in movie_list:
                    if movie_name in self.movies_set or \
                            (movie_list[movie_name] in self.movies_set.values()):
                        continue
                    self.movies_queue.append(movie_name)
                    self.movies_set[movie_name] = movie_list[movie_name]

            # scrap movie info
            while len(self.movies_queue) > 0 and self.curr_movie_num <= self.max_movie_num:

                logging.info('current movie number: ')
                logging.info(self.curr_movie_num)
                movie_name = self.movies_queue[0]
                movie_url = self.movies_set[movie_name]
                self.movies_queue.pop(0)
                if len(movie_url) < 5:
                    continue
                logging.info("$$$")
                logging.info(movie_name)
                logging.info(movie_url)
                movie, actor_list = self.scrap_movie(movie_url, movie_name)
                if len(actor_list) == 0 or (movie['year'] == -1 and movie['gross'] == -1):
                    continue

                self.movies_data.append(movie)
                self.curr_movie_num += 1

                for actor_name_in_list in actor_list:
                    if actor_name_in_list in self.actors_set or \
                            (actor_list[actor_name_in_list] in self.actors_set.values()):
                        continue
                    self.actors_set[actor_name_in_list] = actor_list[actor_name_in_list]
                    self.actors_queue.append(actor_name_in_list)

            self.write_to_json()
            logging.info('write_to_json')
            logging.info(self.curr_actor_num)
            logging.info(self.curr_movie_num)


    def write_to_json(self):
        result = []
        result.append(self.actors_data)
        result.append(self.movies_data)
        with open('data.json', 'w') as fp:
            json.dump(result, fp)


scraper = Scraper(start_url, 126)
scraper.start_scrap()
