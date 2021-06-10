import re
from typing import List

import requests
from bs4 import BeautifulSoup
from bs4.element import ResultSet, Tag
from selenium import webdriver
from salecars.models import Region, City, Models, Marks


class Parser:
    BASE_URL = "https://kolesa.kz"
    HEADERS = {
        "accept": "*/*",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
                      " AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/89.0.4389.90 Safari/537.36",
    }

    def init_url(self, mark, city, price_from, price_to):
        url = f"{self.BASE_URL}/cars/{mark}/{city}/?auto-custom=2&price[from]={price_from}&price[to]={price_to}"
        return url

    def get_html(self, url: str) -> str:
        """Принимает URL-адрес в качестве аргумента запроса,
        возвращает html-страницу из запроса.
        Uses `get()` method from `requests` package
        Args:
            url ([str]): link to the website
        Returns:
            [str]: HTML page from the request
        """
        response = requests.get(url, headers=self.HEADERS)
        html = response.text
        return html

    def pages_count(self, html: str) -> int:
        """Определение количества страниц в каталоге объявления
        Args:
            html (str): The page to search in which
            the value of the last page is being searched
        Returns:
            int: Last page value
        """
        soup = BeautifulSoup(html, "lxml")
        # находим пагинатор с перечислением всех страниц
        paginator = soup.find("div", {"class": "pager"}).find_all("li")

        # если пагинатор найден, то последняя страница равна последнему элементу
        if paginator:
            last_page = int(paginator[-1].text.strip())
        else:
            last_page = 1
        return last_page

    def gather_valuable_data(self, advert: Tag) -> dict[str, ...]:
        """Получение определенных полей в объявлений
        Args:
            advert (Tag): [description]
        Returns:
            Tuple[str, ...]: [description]
        """
        # для выявления паттерна с объемом двигателя
        engine_volume_pattern = re.compile(r"(^\d+.*)(\s)(л$)")
        # все виды топлива указываемые в объявлении
        fuels = ("бензин",  "газ-бензин", "газ")
        # название техники, берем всегда только первые три слова из названия
        vehicle_mark = " ".join(
            advert.find("span", {"class": "a-el-info-title"}).text.split()[:3]
        )
        price = "".join(advert.find("span", {"class": "price"}).text.split()[:-1])
        # блок с описанием объявления
        description = (
            advert.find("div", {"class": "a-search-description"})
            .text.strip()
            .split(",")[:6]
        )
        year = description[0].strip()
        image = advert.find("img").get('src')
        # проверка на соответствие с другими данными,
        # если нет то, второе значение в описании является типом техники
        if (
            description[1].strip() not in fuels
            and re.match(engine_volume_pattern, description[1].strip()) is None
        ):
            vehicle_type = description[1].strip()
        else:
            vehicle_type = ""
        # проверка на соответствие с паттерном объема двигателя
        if re.match(engine_volume_pattern, description[2].strip()):
            engine_volume = description[2].strip()
        elif re.match(engine_volume_pattern, description[1].strip()):
            engine_volume = description[1].strip()
        else:
            engine_volume = ""
        # по умолчанию пустое значение типа топлива
        fuel_type = ""
        # проверка на соответствие с одним из значений топлива
        for target in description[1:]:
            if target.strip() in fuels:
                fuel_type = target.strip()

        data = dict(
            name=vehicle_mark,
            year=year,
            price=price,
            fuel_type=fuel_type,
            engine=engine_volume,
            vehicle_type=vehicle_type,
            image_url=image.replace('160x120.jpg', 'full.jpg')
        )
        return data

    def collect_data(self, adverts: ResultSet) -> list:
        """Сбор всех блоков с объявлениями со страницы
        Args:
            adverts (ResultSet): результат поиска блока с объявлениями
        Returns:
            List: список из объявлении
        """
        collection = []
        for ad in adverts:
            try:
                data = self.gather_valuable_data(ad)
                collection.append(data)
            except AttributeError:
                continue
            except IndexError:
                continue
        return collection

    def start_parsing(self, mark, city, price_from, price_to):
        url = self.init_url(mark, city, price_from, price_to)
        html = self.get_html(url)
        last_page = self.pages_count(html)
        data_collection = []
        for i in range(1, last_page + 1):
            html = self.get_html(f"{self.init_url(mark, city, price_from, price_to)}?page={i}")
            soup = BeautifulSoup(html, "lxml")
            ads_list = soup.find_all("div", {"class": "row vw-item list-item a-elem"})
            data = self.collect_data(ads_list)
            data_collection.extend(data)
        return data_collection


def parse_regions():
    response = requests.get('https://m.kolesa.kz/regions/all/')
    for region in response.json():
        iskz = region.get('isKz')
        if iskz is True:
            Region.objects.create(name=region.get('value'), name_slug=region.get('alias'))
        name = Region.objects.all()
        p = name.values_list('name', flat=True)
        if region.get('parent') is not None and any(region.get('parent') in s for s in p):
            City.objects.create(
                name=region.get('value'),
                name_slug=region.get('alias'),
                region=Region.objects.get(name=region.get('parent'))
            )


def parse_cars():
    response = requests.get('https://m.kolesa.kz/car/brands/?category=auto.car')
    for cars in response.json():
        mark_id = cars.get('id')
        Marks.objects.create(name=cars.get('value'), slug_name=cars.get('name'))
        r = requests.get(f'https://m.kolesa.kz/car/models/{mark_id}/')
        for mod in r.json():
            Models.objects.create(
                name=mod.get('value'),
                slug_name=mod.get('name'),
                mark=Marks.objects.get(name=cars.get('value'))
            )


























