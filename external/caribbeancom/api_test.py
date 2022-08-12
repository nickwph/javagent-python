# coding=utf-8
import datetime
from unittest import TestCase

from external.caribbeancom import api


class Test(TestCase):

    def test_get_item(self):
        item = api.get_item("070116-197")
        self.assertEqual(u"070116-197", item.id)
        self.assertEqual(u"https://www.caribbeancom.com/moviepages/070116-197/index.html", item.url)
        self.assertEqual(u"洗練された大人のいやし亭 〜身も心もチンポも癒されてください〜", item.title)
        self.assertEqual(u"「本日は身も心もチンポも癒されてくださいねぇ」と頭を深々と下げてお辞儀をするAV界を引退してしまった上原亜衣"
                         u"ちゃんが、お客様に極上のおもてなしを披露する為カムバック！お客様の目を見つめて気持ちい部分を確認しながら優"
                         u"しくチク舐め手コキ。口蓋垂で亀頭を刺激させ口内を細めてチンコ全体を締め付けると、お客様は熱い精子を亜衣ちゃ"
                         u"んの口いっぱいにブチまいちゃいます！", item.description)
        self.assertEqual(u"https://smovie.caribbeancom.com/moviepages/070116-197/images/jacket.jpg", item.poster_url)
        self.assertEqual(u"https://smovie.caribbeancom.com/moviepages/070116-197/images/l_l.jpg", item.background_url)
        self.assertEqual(u"https://www.caribbeancom.com/search_act/6706/1.html", item.actor_url)
        self.assertEqual(u"上原亜衣", item.actor_name)
        self.assertEqual(6706, item.actor_id)
        self.assertEqual(u"https://www.caribbeancom.com/box/search_act/6706/images/top.jpg",
                         item.actor_large_picture_url)
        self.assertEqual(u"https://www.caribbeancom.com/images/actress/50x50/actor_6706.jpg",
                         item.actor_small_picture_url)
        self.assertEqual(u"https://smovie.caribbeancom.com/sample/movies/070116-197/480p.mp4", item.sample_video_url)
        self.assertEqual(datetime.date(2016, 7, 1), item.upload_date)
        self.assertEqual(datetime.time(1, 1, 1), item.duration)
        self.assertEqual(3661, item.duration_in_seconds)
        self.assertEqual(u"洗練された大人のいやし亭", item.series_name)
        self.assertEqual(960, item.series_id)
        self.assertEqual(u"https://www.caribbeancom.com/series/960/index.html", item.series_url)
        self.assertEqual(2, len(item.tags))
        self.assertEqual(u"オリジナル動画", item.tags[0].name)
        self.assertEqual(u"original", item.tags[0].slug)
        self.assertEqual(u"https://www.caribbeancom.com/listpages/original1.htm", item.tags[0].url)
        self.assertEqual(7, len(item.genres))
        self.assertEqual(u"中出し", item.genres[0].name)
        self.assertEqual(u"creampie", item.genres[0].slug)
        self.assertEqual(u"https://www.caribbeancom.com/listpages/creampie1.htm", item.genres[0].url)
        self.assertEqual(5, item.rating)

    def test_get_item_without_series(self):
        item = api.get_item("052716-172")
        self.assertEqual(u"052716-172", item.id)
        self.assertEqual(u"https://www.caribbeancom.com/moviepages/052716-172/index.html", item.url)
        self.assertEqual(u"ものすごい三穴蹂躙", item.title)

    def test_extract_id(self):
        self.assertEqual("123123-233", api.extract_id("carib-123123-233"))
        self.assertEqual("123123-233", api.extract_id("Carib-123123-233"))
        self.assertEqual("123123-233", api.extract_id("Carib-123123-233-asd"))
        self.assertEqual("123123-233", api.extract_id("Carib-123123-233-FHD"))
        self.assertEqual(None, api.extract_id("Carib-12123-233-FHD"))
        self.assertEqual("123123-23123123", api.extract_id("Carib-123123-23123123-FHD"))
        self.assertEqual("123123-1", api.extract_id("Carib-123123-1-FHD"))
        self.assertEqual("123123-1", api.extract_id("Caribbean-123123-1-FHD"))
        self.assertEqual("123123-1", api.extract_id("Caribbeancom-123123-1-FHD"))
        self.assertEqual(None, api.extract_id("Caribb-123123-1-FHD"))
        self.assertEqual(None, api.extract_id("Caribbeanc-123123-1-FHD"))

    def test_has_valid_id(self):
        self.assertEqual(True, api.has_valid_id("carib-123123-233"))
        self.assertEqual(True, api.has_valid_id("Carib-123123-233"))
        self.assertEqual(True, api.has_valid_id("Carib-123123-233-asd"))
        self.assertEqual(True, api.has_valid_id("Carib-123123-233-FHD"))
        self.assertEqual(False, api.has_valid_id("Carib-12123-233-FHD"))
        self.assertEqual(True, api.has_valid_id("Carib-123123-23123123-FHD"))
        self.assertEqual(True, api.has_valid_id("Carib-123123-1-FHD"))
        self.assertEqual(True, api.has_valid_id("Caribbean-123123-1-FHD"))
        self.assertEqual(True, api.has_valid_id("Caribbeancom-123123-1-FHD"))
        self.assertEqual(False, api.has_valid_id("Caribb-123123-1-FHD"))
        self.assertEqual(False, api.has_valid_id("Caribbeanc-123123-1-FHD"))
