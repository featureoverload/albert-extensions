"""translation module.
Synopsis: <triger> <word>
"""

import os
import locale
import json
import urllib.parse
import hashlib
# from textwrap import dedent

from albertv0 import *
import requests

__iid__ = "PythonInterface/v0.1"
__prettyname__ = "Translation Word"
__trigger__ = "tr "
__version__ = "2.3"
__author__ = "Joseph Lin"
__dependencies__ = ["requests", "youdao account"]

ICON_PATH = iconLookup("albert")
TO_LANG = 'zh'

WORDS_DATA_SRC_URL = "n/a"
WORDS_DATA_SRC_PATH = "/usr/share/dict/words"
WORDS_DATA_PATH = os.path.join(dataLocation(), "words.txt")
WORDS_CACHE = None


def initialize():
    global TO_LANG, WORDS_CACHE
    try:
        TO_LANG = locale.getdefaultlocale()[0].split('_')[0]  # cat /etc/locale.gen
    except Exception as err:
        warning(err)

    try:
        with open(WORDS_DATA_SRC_PATH, "r") as fp:
            WORDS_CACHE = [_.strip() for _ in fp.readlines()]
    except Exception as err:
        warning(err)


def get_completes(key):
    global WORDS_CACHE  # 因为我们不需要修改它，所以本行也可以省略。
    right = len(WORDS_CACHE) - 1  # 通常需要考虑“输入”列表的边界！
    left = 0
    start = -1
    while left <= right:
        '''起始位置的特点：
          WORDS_CACHE[start].startswith(key) （WORDS_CACHE[start] >= key）
          WORDS_CACHE[start - 1] < key
        '''
        middle = (right + left) // 2  # 可以写成 (right + left) >> 1。
        if WORDS_CACHE[middle] > key:
            if WORDS_CACHE[middle - 1] < key:
                if WORDS_CACHE[middle].startswith(key):
                    start = middle
                    break
                break
            right = middle - 1
        elif WORDS_CACHE[middle] < key:
            if WORDS_CACHE[middle + 1] > key:
                if WORDS_CACHE[middle + 1].startswith(key):
                    start = middle + 1
                    break
            left = middle + 1
        else:
            start = middle
            break
    results = []
    if start != -1:
        i = 0
        while WORDS_CACHE[start + i].startswith(key):
            results.append(WORDS_CACHE[start + i])
            i += 1
    return results


class YouDaoAPI():
    ua = ("Mozilla/5.0 (Windows NT 10.0; WOW64) "
          "AppleWebKit/537.36 (KHTML, like Gecko) "
          "Chrome/62.0.3202.62 Safari/537.36")
    urltmpl = ("http://openapi.youdao.com/api"
               "?appKey={}"
               "&q={}&from=auto&to={}"
               "&salt={}&sign={}")
    langSupported = dict.fromkeys(('zh', 'en', 'es', 'fr',
                                   'ko', 'ja', 'ru', 'pt'))

    def __init__(self, word):
        self.word = word

    def get_url(self, src, dst, txt):
        ''' 按有道的格式生成请求地址。src为源语言，dst为目标语言 '''
        appKey = os.environ.get('YOUDAO_APPID')  # 注册智云后获得
        secretKey = os.environ.get('YOUDAO_APPKEY')
        salt = '123456'  # TODO: 使用随机数
        sign = appKey + txt + salt + secretKey
        m1 = hashlib.md5()
        m1.update(sign.encode(encoding='utf-8'))
        sign = m1.hexdigest()
        q = urllib.parse.quote_plus(txt)
        url = self.urltmpl.format(appKey, q, dst, salt, sign)
        return url

    def get_result_from_api_as_dict(self):
        url = self.get_url('auto', TO_LANG, self.word)
        req = requests.get(url, headers={'User-Agent': self.ua})
        return json.loads(req.text)


def generate_display_items(data):
    results = []
    if set({'web', 'phonetic', 'basic'}) & set(data.keys()):
        try:
            results.append(  # 发音
                Item(id="", icon=ICON_PATH,
                     completion="", urgency=ItemBase.Notification,
                     text=str(data['basic']['phonetic']),
                     subtext="phonetic",
                     actions=[]))
        except Exception:
            pass

        try:
            for explain in data['basic']['explains']:  # 释义
                results.append(
                    Item(id="", icon=ICON_PATH,
                         completion="", urgency=ItemBase.Notification,
                         text=str(explain), subtext='explain',
                         actions=[ClipAction("copy", str(explain)), ]))
        except Exception:
            pass

        try:
            for web_expl in data['web']:  # 网络释义
                results.append(
                    Item(id="", icon=ICON_PATH,
                         completion="", urgency=ItemBase.Notification,
                         text="{}: {}".format(web_expl['key'], web_expl['value']),
                         subtext='web explain',
                         actions=[ClipAction("copy", str(web_expl['value'])), ]))
        except Exception:
            pass

        return results

    raise RuntimeError("no result")


def handleQuery(query):
    if not query.isValid or not query.isTriggered or len(query.string) <= 1:
        return

    # info(query.string)
    qs = query.string.split('|')
    err_msg = Item(id="", icon=ICON_PATH, actions=[],
                   completion="", urgency=ItemBase.Notification,
                   text="", subtext="")
    items = [err_msg, ]

    if len(qs) <= 1:
        try:
            list_ = []
            for complete in get_completes(qs[0]):
                list_.append(Item(
                    id="", icon=ICON_PATH, actions=[],
                    text=complete, subtext="autocomplete",
                    completion="", urgency=ItemBase.Notification))
            items = list_
        except Exception as err:
            warning("{!r}".format(err))
            items[0].text = str(err)
            items[0].subtext = "Generate complete items Error"

        return items

    if qs[1]:
        if qs[1] == 'z':
            try:
                data = YouDaoAPI(qs[0]).get_result_from_api_as_dict()
                items = generate_display_items(data)
            except Exception as err:
                warning("{!r}".format(err))
                items[0].text = str(err)
        # elif qs[1] == 'e':  # zh to en
        else:
            items[0].text = "Not Support Action - '{}'".format(qs[1])
            items[0].subtext = "Command Error"
    else:
        try:
            # support_actions = []
            items[0].text = "z - to 'zh'"
            # items[1].text = "e - to 'en'"
        except Exception as err:
            items[0].text = str(err)

    return items
