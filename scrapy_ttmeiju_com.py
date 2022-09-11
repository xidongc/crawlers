# -*- coding: utf-8 -*-
'''
Author Xidong, 2016/10/1 Web Spider for 天天美剧
getting info from url based on pages, using re to match
'''

import urllib2
import re

# example website to fetch:
# url = 'http://www.ttmeiju.com/seed/64694.html'

base_url = 'http://www.ttmeiju.com/seed/'
pages = range(63001,63100)

try:
    for page in pages:
        url = base_url+str(page)+'.html'
        request = urllib2.Request(url)
        response = urllib2.urlopen(request)
        content = response.read().decode('gbk')

        # can see raw html page by print content
        # print content

        # start fetching create date and last update date date format dddd-dd-dd dd:dd:dd
        pattern_date = re.compile('\d{4}-\d{2}-\d{2} \d{2}:\d{2}',re.S)
        date_tmp = re.findall(pattern_date,content)
        if date_tmp.__len__() is 2:
            create_date = date_tmp[0].encode('utf-8')
            last_update = date_tmp[1].encode('utf-8')
        else:
            create_date = ' '
            last_update = ' '

        # start fetching image url for specific movie format http://w+.jpg
        pattern_image = re.compile('(?<=src=")[^\s]+(?="\sid="spic")',re.S)
        image_tmp = re.findall(pattern_image,content)
        if image_tmp.__len__() is not 0:
            image = image_tmp[0].encode('utf-8')
        else:
            image = ' '

        # start fetching download link in baidu yun, Can also fetch also download link but not in this app
        pattern_bd_link = re.compile("https://pan\.baidu\.com.*?(?=')", re.S)
        bd_link_tmp = re.findall(pattern_bd_link,content)
        if bd_link_tmp.__len__() is not 0:
            bd_link = bd_link_tmp[0].encode('utf-8')

        # start fetching name which include episode/chinese name/english name/resolution of a specific movie
        pattern_name = re.compile('(?<=title>).*(?=</title>)', re.S)
        names = re.findall(pattern_name, content)

        # chinese name
        if names.__len__() is not 0:
            name_ch = names[0].encode('utf-8').split(' ')[0]

            #english name because it may contain ' ', use re to match
            pattern_name_en = re.compile('\w[\w,\s]*(?=\sS\d{2}E\d{2})', re.S)
            if re.findall(pattern_name_en, names[0]):
                name_en = re.findall(pattern_name_en, names[0])[0].encode('utf-8')

            # episode name format SddEdd
            pattern_episode = re.compile('S\d{2}E\d{2}', re.S)
            if re.findall(pattern_episode, names[0]):
                episode = re.findall(pattern_episode, names[0])[0].encode('utf-8')

            #resolution for a movie like 720p default is 480p if nothing specified
            pattern_resolution = re.compile('\d+p')
            if re.findall(pattern_resolution, names[0]):
                resolution = re.findall(pattern_resolution, names[0])[0].encode('utf-8')
            else:
                resolution = '480p'

        print name_ch+'   '+name_en+'   '+ episode+'   ' + bd_link+'   '+resolution+'   '+image+ '   '+create_date+'   '+ last_update

#error handling
except urllib2.URLError, e:
    if hasattr(e, "code"):
        print e.code
    if hasattr(e, "reason"):
        print e.reason