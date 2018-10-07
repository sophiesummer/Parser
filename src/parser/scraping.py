from bs4 import BeautifulSoup
import urllib
from src.graph.Graph import Graph, Actor, Movie


start_url = "https://en.wikipedia.org/wiki/Morgan_Freeman"
pre_url = "https://en.wikipedia.org"
present_year = 2018


def make_soup(url):
    pages = urllib.request.urlopen(url)
    soup_data = BeautifulSoup(pages, "html.parser")
    return soup_data


class Scraper:
    def __init__(self, start_url, max_movie_num):
        self.actors_set = {} # name : url
        self.movies_set = {}
        self.max_actor_num = max_movie_num * 2
        self.max_movie_num = max_movie_num
        self.actors_queue = [] # actor_name
        self.movies_queue = [] # movie_name
        self.graph = Graph()
        self.start_url = start_url

    def scrap_actor(self, actor_url, actor_name):
        soup = make_soup(actor_url)
        actor = Actor()
        actor.name = actor_name
        try:
            born_info = soup.soup.find('table', {"class": 'infobox biography vcard'}).\
                find('tbody').find('th', text=('Born')).find_parent('tr').\
                find('span', {'class': "bday"}).text
        except:
            actor.birthday = ""
            actor.age = -1
        else:
            actor.birthday = born_info
            actor.age = present_year - int(born_info[:4])

        movie_list = {}
        try:
        # if filmography is an outside page
            film_list = soup.find('div', {'id': 'mw-content-text'}). \
                find('div', {'class': 'mw-parser-output'}). \
                find_all("div", {"role": "note"})

            for f in film_list:
                if "Main article" in f.text:
                    href = f.find('a')
                    new_page = href.get('href')
                    break

            new_page = pre_url + new_page
            film_page_body = make_soup(new_page).find("div", {"class": "mw-parser-output"})
            film_table = film_page_body.find("table", {'class': 'wikitable plainrowheaders sortable'}). \
                find("tbody")


            for tr in film_table.find_all('tr'):
                each_film = tr.find("a")
                # try
                if each_film:
                    film_web = each_film.get('href')  # without prehref
                    film_web = pre_url + film_web
                    film_name = each_film.text
                    movie_list[film_name] = film_web
        except:
            # if filmgraphy is inside the webpage
            try:
                film_table = soup.find('table', {'class': 'wikitable sortable'}).\
                    find('tbody').find_all('tr')
                for tr in film_table:
                    each_film = tr.find("a")
                    # try
                    if each_film:
                        film_web = each_film.get('href')  # without prehref
                        film_web = pre_url + film_web
                        film_name = each_film.text
                        movie_list[film_name] = film_web
            except:
                print("none filmgraphy")

        return actor, movie_list

    def scrap_movie(self, movie_url, movie_name):
        soup = make_soup(movie_url)
        movie = Movie()
        movie.name = movie_name

        movie_info = soup.find('table', {"class": "infobox vevent"}).find('tbody')
        box_office_title = movie_info.find('th', text=("Box office"))
        box_office = box_office_title.find_parent('tr').find('td').contents[0]
        movie.gross = self.box_office_format(box_office) # change to number function

        release_date = movie_info.find('th', text=("Release date")).find_parent('tr').\
            find('span', {'class': 'bday dtstart published updated'}).text
        movie.year = int(release_date[:4])

        actor_list = {}
        star_list = movie_info.find('th', text=('Starring')).find_parent('tr').find_all('a')
        for a in star_list:
            actor_name = a.text
            actor_link = a.get('href')
            actor_link = pre_url + actor_link
            actor_list[actor_name] = actor_link

        return movie, actor_list

    def box_office_format(self, box_office):
        start = box_office.index("$")
        box_office = box_office[start + 1:]
        box_office = box_office.replace(',', '')

        gross = -1
        if "million" in box_office:
            end = box_office.index('million')
            box_office = box_office[:end - 1]
            gross = int(box_office) * 10**6
        elif "billion" in box_office:
            end = box_office.index('billion')
            box_office = box_office[:end - 1]
            gross = int(box_office) * 10**9
        else:
            gross = int(box_office)

        return gross

    def start_scrap(self):
        self.actors_set["Morgan Freeman"] = self.start_url
        self.actors_queue.append("Morgan Freeman")
        while len(self.actors_set) < self.max_actor_num or \
                (len(self.movies_set) < self.max_movie_num):

            actor_name = self.actors_queue[0]
            actor_url = self.actors_set[actor_name]
            self.actors_queue.pop(0)
            if len(actor_url) < 5:
                continue

            actor, movie_list = self.scrap_actor(actor_url, actor_name)
            self.graph.add_actor(actor)

            for movie_name in movie_list:
                if len(movie_list[movie_name]) < 5:
                    continue
                movie, actor_list = self.scrap_movie(movie_list[movie_name], movie_name)
                self.graph.add_movie(movie)
                self.graph.add_edges(actor, movie)
                self.movies_set[movie_name] = movie_list[movie_name]

                for actor_name_in_list in actor_list:
                    self.actors_set[actor_name_in_list] = actor_list[actor_name_in_list]
                    self.actors_queue.append(actor_name_in_list)

        return self.graph


