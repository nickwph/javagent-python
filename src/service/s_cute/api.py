# coding=utf-8
import datetime
import re
from pyquery import PyQuery
from typing import List

base_url = "https://www.s-cute.com"


def extract_id(filename):
    """
    :type filename: str
    :rtype: str
    """
    match = re.findall("s-cute-(.*?)$", filename, re.IGNORECASE)
    if len(match) > 0: return match[0]  # noqa
    return None


def get_by_id(product_id):
    """
    :type product_id: str
    """
    product_id = product_id.lower()
    url = "{}/contents/{}".format(base_url, product_id)
    query = PyQuery(url)

    item = SCuteItem()
    item.id = product_id
    item.url = url
    item.title = query('h3.h1').text()
    item.description = query('.blog-single > p').text()
    item.cover_url = query('.content-cover > img:first').attr('src')
    item.duration_in_min = int(re.findall(r"\d+", query(".blog-single .meta .comment").text())[0])
    item.photo_count = int(re.findall(r"\d+", query(".blog-single .meta .views").text())[0])

    actress_id_and_name = query('.about-author h5').text()
    actress_id_and_name = re.findall(r"#(\d+)\s(.*?)$", actress_id_and_name)
    item.actress.id = int(actress_id_and_name[0][0])
    item.actress.name = actress_id_and_name[0][1]
    item.actress.description = query('.about-author p:last').text()
    item.actress.url = "{}{}".format(base_url, query('.about-author a:first').attr('href'))
    item.actress.photo_url = query('.about-author img').attr('src')

    date = query(".blog-single .meta .date").text()
    date = re.findall(r"\d+/\d+/\d+", date)[0]
    item.release_date = datetime.datetime.strptime(date, '%Y/%m/%d')  # query(".blog-single .meta .date").text()

    for element in query(".tags a"):
        tag = SCuteItem.Tag()
        tag.name = element.text
        tag.url = element.attrib['href']
        item.tags.append(tag)

    for element in query(".photos a[data-lightbox='gallery']"):
        photo = SCuteItem.Photo()
        photo.image_url = element.attrib['href']
        photo.thumbnail_url = PyQuery(element).find('img').attr('src')
        item.photos.append(photo)

    return item


class SCuteSearchResultItem(object):
    def __init__(self):
        self.id = "Stub"
        self.url = "Stub"
        self.title = "Stub"
        self.thumbnail_url = "Stub"
        self.upload_year = 0  # Stub


class SCuteItem(object):
    def __init__(self):
        self.id = "Stub"
        self.url = "Stub"
        self.title = "Stub"
        self.description = "Stub"
        self.cover_url = "Stub"
        self.duration_in_min = 0  # Stub
        self.photo_count = 0  # Stub
        self.release_date = datetime.datetime.now()  # Stub
        self.actress = SCuteItem.Actress()
        self.tags = []  # type: List[SCuteItem.Tag]
        self.photos = []  # type: List[SCuteItem.Photo]

    class Actress(object):
        def __init__(self):
            self.id = 0
            self.name = "Stub"
            self.url = "Stub"
            self.description = "Stub"
            self.photo_url = "Stub"

    class Tag(object):
        def __init__(self):
            self.name = "Stub"
            self.url = "Stub"

    class Photo(object):
        def __init__(self):
            self.image_url = "Stub"
            self.thumbnail_url = "Stub"
