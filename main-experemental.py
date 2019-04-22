# coding=utf8
import json
import re
import time

import requests

import attachmentslib

with open('vk_conf.json') as vk_json:
    PAYLOAD = json.load(vk_json)

with open('discord_webhooks.json') as webhooks_json:
    WEBHOOKS = json.load(webhooks_json)

URL = 'https://api.vk.com/method/wall.get'
LATEST_RECEIVED = 'none'


def main():
    global LATEST_RECEIVED
    data = requests.get(URL, params=PAYLOAD).json()
    if '#art' in data['response']['items'][0]['text']:
        webhook_url = WEBHOOKS["webhook_art"]
        ping_message = ""
    else:
        webhook_url = WEBHOOKS["webhook"]
        ping_message = "heyooo"

        # "<@&562705250470068248>"

    if LATEST_RECEIVED != data['response']['items'][0]['id']:

        data['response']['items'][0]['text'] = re.sub(r"#\w+@?\w+", "", data['response']['items'][0]['text'])
        data['response']['items'][0]['text'] = re.sub(r"\[.*?\||\]", "", data['response']['items'][0]['text'])
        # data['response']['items'][0]['text'] = re.sub(r"(^|\s)((https?:\/\/)?[\w-]+(\.[a-z-]+)+\.?(:\d+)?(\/\S*)?)", "", data['response']['items'][0]['text'])
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
        LATEST_RECEIVED = data['response']['items'][0]['id']

    else:
        pass


if __name__ == '__main__':
    while True:
        main()
        time.sleep(600)
