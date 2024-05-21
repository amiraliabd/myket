from .exceptions import ImdbConnectionFailError
import bs4
import requests
import typing


class CrullerCore:
    _base_url = 'https://www.imdb.com/'

    def __init__(self, movie_code):
        self._movie_code = movie_code
        self._movie_soup = self._get_soup(movie_code)

    def _get_soup(self, movie_code) -> bs4.BeautifulSoup:
        page = requests.get(
            self._base_url + f"title/{movie_code}",
            headers={'User-Agent': 'Mozilla/5.0'},
        )
        if page.status_code != 200:
            raise ImdbConnectionFailError(
                "Can't connect to imdb.com."
                " Service might be down or filtered for current location. Please try again later."
            )

        return bs4.BeautifulSoup(page.text, "html.parser")

    def get_similar(self) -> typing.List[str]:
        similar_soup = self._movie_soup.find(
            "section", {"data-testid": "MoreLikeThis"}
        ).findAll(
            "a", {"class": "ipc-poster-card__title ipc-poster-card__title--clamp-2 ipc-poster-card__title--clickable"}
        )
        similar_movie_code = []
        for similar in similar_soup:
            similar_movie_code.append(similar.get("href").split("/")[2])
        return similar_movie_code

    def get_title(self) -> str:
        return self._movie_soup.find('head').find('title').get_text()

    def get_images(self) -> typing.List[str]:
        image_links = []
        photos = self._movie_soup.find("section", {"data-testid": "Photos"}).findAll("img", )
        for photo in photos:
            image_links.append(photo.get("src"))
        return image_links

    def get_storyline(self) -> str:
        summary_soup = self._get_soup(f'{self._movie_code}/plotsummary')
        storyline = summary_soup.find(
            'div', {"data-testid": "sub-section-summaries"}
        ).find('div', {'class': 'ipc-html-content-inner-div'}).get_text()

        return storyline
