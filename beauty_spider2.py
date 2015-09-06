# -*- coding: utf-8 -*-


import re
import urllib2
import sys
import download_beauty


comment_regex = re.compile(u'class="nrec"><span class="hl (f\d)">(\w+)?')
url_regex = re.compile(r'<a href="([^"]+)">')


def reformalize(level):
    if level is None:
        return 100
    elif level[0] == 'X':
        return -10 * int(level[1])


def getFirstPage():
    content = urllib2.urlopen('https://www.ptt.cc/bbs/Beauty/index.html').read()
    first_page = re.search(r'href="/bbs/Beauty/index(\d+).html">&lsaquo;', content).group(1)
    return int(first_page)


def crawPage(url, article_list, push_rate):
    try:
        source = urllib2.urlopen(url)
        content = source.read()
    except urllib2.URLError as urlerr:
        print "URLError detected: " + url
        return

    rent_lst = content.split('<div class="r-ent">')

    for each_data in rent_lst:
        comment_rate = comment_regex.search(each_data)

        if comment_rate:
            try:
                rate = int(comment_rate.group(2))
            except Exception as err:
                rate = reformalize(comment_rate.group(2))
            if rate >= push_rate:
                # parse each url
                # get into new page, parse photo
                try:
                    url = 'https://www.ptt.cc/' + url_regex.search(each_data).group(1)
                    article_list.append((rate, url))
                    # print rate, url
                except Exception as err:
                    # print err
                    pass


if __name__ == '__main__':

    start_page, page_term, push_rate = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])
    if start_page < 0:
        start_page = getFirstPage()
    # print start_page, page_term, push_rate

    print "解析下載網頁面，統計數量中..."

    article_list = []
    for page in range(start_page, start_page - page_term, -1):
        page_url = 'https://www.ptt.cc/bbs/Beauty/index' + str(page) + '.html'
        crawPage(page_url, article_list, push_rate)

    print "即將開始下載圖片, 請再等一下下 ^_^"

    total = len(article_list)
    count = 0
    for hot_rate, article in article_list:
        download_beauty.store_pic(article, str(hot_rate))
        count += 1
        print "已經下載: " + str(100 * count / total ) + " %."

    print "即將下載完畢，滿滿的正妹圖就要入袋拉！"
