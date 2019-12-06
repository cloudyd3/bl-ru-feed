# coding=utf8
import json
import re
import time

import requests

import attachmentslib

with open('vk.json') as vk:
    vk_conf = json.load(vk)

with open('discord.json') as discord:
    discord_hooks = json.load(discord)

def main():
    URL = 'https://api.vk.com/method/wall.get'
    PAYLOAD = {
        "domain": "borderlands",
        "count": 1,
        "filter": "owner",
        "extended": 1,
        "offset": 0,
        "access_token": vk_conf["access_token"],
        "v": 5.95
    }
    data = requests.get(URL, params=PAYLOAD).json()
    if data['response']['items'][0].get('is_pinned'):
        PAYLOAD = {
            "domain": "borderlands",
            "count": 1,
            "filter": "owner",
            "extended": 1,
            "offset": 1,
            "access_token": vk_conf["access_token"],
            "v": 5.95
        }
        data = requests.get(URL, params=PAYLOAD).json()

    if ('#art' in data['response']['items'][0]['text'].casefold()) or (
            '#cosplay' in data['response']['items'][0]['text'].casefold()):
        webhook_url = discord_hooks["webhook_2"]
        ping_message = ""
    else:
        webhook_url = discord_hooks["webhook_1"]
        ping_message = "<@&562705250470068248>"
    log = open('posted_log')
    if str(data['response']['items'][0]['id']) in log.read():
        print('Already posted, skipping')
        log.close()
        pass
    else:
        data['response']['items'][0]['text'] = re.sub(r"#\w+@?\w+", "", data['response']['items'][0]['text'])
        data['response']['items'][0]['text'] = re.sub(r"\[.*?\||\]", "", data['response']['items'][0]['text'])
        data['response']['items'][0]['text'] = data['response']['items'][0]['text'].replace('\n\n', '\n')

        request = {"content": ping_message, "embeds": []}

        if len(data['response']['items'][0]['text']) > 2000:
            try:
                profile_icon = data['response']['profiles'][0]['photo_100']
                profile_name = '{} {}'.format(data['response']['profiles'][0]['first_name'],
                                              data['response']['profiles'][0]['last_name'])
            except IndexError:

                profile_icon = ""
                profile_name = ""
            splitted_text = data['response']['items'][0]['text'].split('\n')
            embed = {
                "footer": {
                    "icon_url": profile_icon,
                    "text": profile_name,
                },
                "description": '{}'.format(splitted_text[0]),
                "author": {
                    "url": "https://vk.com/{}?w=wall-{}_{}".format(data['response']['groups'][0]['screen_name'],
                                                                   data['response']['groups'][0]['id'],
                                                                   data['response']['items'][0]['id']),
                    "name": data['response']['groups'][0]['name'],
                    "icon_url": data['response']['groups'][0]['photo_50']
                },
                "color": 4880040,
            }
            request["embeds"].append(embed)
            for i in splitted_text:
                if i == splitted_text[0]:
                    pass
                if i == '\n':
                    pass
                if i == '  ':
                    pass
                else:
                    embed = {
                        "description": i
                    }
                    request["embeds"].append(embed)

        else:
            try:
                profile_icon = data['response']['profiles'][0]['photo_100']
                profile_name = '{} {}'.format(data['response']['profiles'][0]['first_name'],
                                              data['response']['profiles'][0]['last_name'])
            except IndexError:

                profile_icon = ""
                profile_name = ""
            embed = {
                "footer": {
                    "icon_url": profile_icon,
                    "text": profile_name,
                },
                "description": data['response']['items'][0]['text'],
                "author": {
                    "url": "https://vk.com/{}?w=wall-{}_{}".format(data['response']['groups'][0]['screen_name'],
                                                                   data['response']['groups'][0]['id'],
                                                                   data['response']['items'][0]['id']),
                    "name": data['response']['groups'][0]['name'],
                    "icon_url": data['response']['groups'][0]['photo_50']
                },
                "color": 4880040,
            }
            request["embeds"].append(embed)

        try:
            repost = data['response']['items'][0]['copy_history'][0]

            embed_repost = {
                "footer": {
                    "icon_url": data['response']['profiles'][0]['photo_100'],
                    "text": '{} {}'.format(data['response']['profiles'][0]['first_name'],
                                           data['response']['profiles'][0]['last_name']),
                },
                "description": repost['text'],
                "author": {
                    "url": "https://vk.com/{}?w=wall-{}_{}".format(data['response']['groups'][1]['screen_name'],
                                                                   data['response']['groups'][1]['id'],
                                                                   repost['id']),
                    "name": data['response']['groups'][1]['name'],
                    "icon_url": data['response']['groups'][1]['photo_50']
                },
                "color": 4880040,
                "thumbnail": {
                    "url": "https://image.flaticon.com/icons/png/24/60/60577.png",
                }
            }

            request["embeds"].append(embed_repost)
            attachments = data['response']['items'][0]['copy_history'][0]
            attachmentslib.merge_attachments(attachments, request)
        except KeyError:
            pass

        attachments = data['response']['items'][0]
        attachmentslib.merge_attachments(attachments, request)

        print(json.dumps(request))

        try:
            r = requests.post(webhook_url, data=json.dumps(request), headers={"Content-Type": "application/json"})
            r.raise_for_status()
        except requests.exceptions.HTTPError as err:
            print(err)
        log.close()
        log = open('posted_log', 'a+')
        log.write(str(data['response']['items'][0]['id']))
        log.write('\n')
        log.close()

if __name__ == '__main__':
    while True:
        main()
        time.sleep(300)
