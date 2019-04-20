# coding=utf8
import json
import re
import time

import requests

with open('vk_conf.json') as vk_json:
    PAYLOAD = json.load(vk_json)

with open('discord_webhooks.json') as webhooks_json:
    WEBHOOKS = json.load(webhooks_json)

URL = 'https://api.vk.com/method/wall.get'
LATEST_RECEIVED = 'none'


def main():
    global LATEST_RECEIVED, attachments
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
        # data['response']['items'][0]['text'] = re.sub(r"(^|\s)((https?:\/\/)?[\w-]+(\.[a-z-]+)+\.?(:\d+)?(\/\S*)?)", "", data['response']['items'][0]['text'])
        data['response']['items'][0]['text'] = data['response']['items'][0]['text'].replace('\n\n', '\n')

        request = {"content": ping_message, "embeds": []}

        if len(data['response']['items'][0]['text']) > 2000:
            splitted_text = data['response']['items'][0]['text'].split('\n')
            embed = {
                "footer": {
                    "icon_url": data['response']['profiles'][0]['photo_100'],
                    "text": '{} {}'.format(data['response']['profiles'][0]['first_name'],
                                           data['response']['profiles'][0]['last_name']),
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
            embed = {
                "footer": {
                    "icon_url": data['response']['profiles'][0]['photo_100'],
                    "text": '{} {}'.format(data['response']['profiles'][0]['first_name'],
                                           data['response']['profiles'][0]['last_name']),
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
            attachments = data['response']['items'][0]['attachments']
        except KeyError:
            pass

        try:
            repost = data['response']['items'][0]['copy_history'][0]
            embed = {
                "thumbnail": {
                    "url": "https://image.flaticon.com/icons/png/24/60/60577.png",
                },
                "description": "[Репост](https://vk.com/borderlands?w=wall{}_{})".format(repost['owner_id'],
                                                                                         repost['id']),
                "color": 4880040
            }
            request["embeds"].append(embed)
        except KeyError:
            pass

        try:
            for i in range(len(attachments)):
                if attachments[i]['type'] == 'audio_playlist':
                    fields = []
                    for n in range(len(attachments[i]['audio_playlist']['audios'])):
                        songs = {
                            "name": attachments[i]['audio_playlist']['audios'][n]['title'],
                            "value": "by {}".format(attachments[i]['audio_playlist']['audios'][n]['artist']),
                        }
                        fields.append(songs)
                    embed = {
                        "thumbnail": attachments[i]['audio_playlist']['photo']['photo_300'],
                        "title": "**{}**".format(attachments[i]['audio_playlist']['title']),
                        "url": "https://vk.com/audio?z=audio_playlist{}_{}".format(
                            attachments[i]['audio_playlist']['owner_id'],
                            attachments[i]['audio_playlist']['id']),
                        "fields": fields,
                        "color": 4880040
                    }
                    request["embeds"].append(embed)
                if attachments[i]['type'] == 'photo':
                    embed = {
                        "image": {
                            "url": attachments[i]['photo']['sizes'][
                                len(attachments[i]['photo']['sizes']) - 1]['url']
                        },
                        "color": 4880040
                    }
                    request["embeds"].append(embed)
                if attachments[i]['type'] == 'doc':
                    if attachments[i]['doc']['type'] == 4:
                        embed = {
                            "image": {
                                "url": attachments[i]['doc']['url']
                            },
                            "color": 4880040
                        }
                        request["embeds"].append(embed)

                    if attachments[i]['doc']['type'] == 3:
                        print(len(attachments[i]['doc']['preview']['photo']['sizes']))
                        print(i)
                        embed = {
                            "image": {
                                "url": attachments[i]['doc']['preview']['photo']['sizes'][
                                    len(attachments[i]['doc']['preview']['photo']['sizes']) - 1]['src'],
                            },
                            "color": 4880040
                        }
                        request["embeds"].append(embed)
                if attachments[i]['type'] == 'video':
                    embed = {
                        "image": {
                            "url": attachments[i]['video']['first_frame_720']
                        },
                        "color": 4880040
                    }
                    request["embeds"].append(embed)
                if attachments[i]['type'] == 'poll':
                    fields = []
                    for n in range(len(attachments[i]['poll']['answers'])):
                        answer_field = {
                            "name": attachments[i]['poll']['answers'][n]['text'],
                            "value": "{} голосов, {}% всех проголосовавших".format(
                                attachments[i]['poll']['answers'][n]['votes'],
                                attachments[i]['poll']['answers'][n]['rate']),
                        }
                        fields.append(answer_field)
                    try:
                        embed = {
                            "title": "**{}**".format(attachments[i]['poll']['question']),
                            "url": "https://vk.com/poll{}_{}".format(attachments[i]['poll']['owner_id'],
                                                                     attachments[i]['poll']['id']),
                            "image": {
                                "url": attachments[i]['poll']['photo']['images'][0]['url']
                            },
                            "fields": fields,
                            "color": 4880040
                        }
                        request["embeds"].append(embed)
                    except KeyError:
                        embed = {
                            "title": "**{}**".format(attachments[i]['poll']['question']),
                            "url": "https://vk.com/poll{}_{}".format(attachments[i]['poll']['owner_id'],
                                                                     attachments[i]['poll']['id']),
                            "fields": fields,
                            "color": 4880040
                        }
                        request["embeds"].append(embed)
                if attachments[i]['type'] == 'link':
                    embed = {
                        "thumbnail": {
                            "url": "https://image.flaticon.com/icons/png/24/61/61020.png",
                        },
                        "description": "**[{}]({})**".format(attachments[i]['link']['title'],
                                                             attachments[i]['link']['url']),
                        "image": {
                            "url": attachments[i]['link']['photo']['sizes'][2]['url']
                        },
                        "color": 4880040
                    }
                    request["embeds"].append(embed)
                else:
                    pass
        except NameError:
            pass

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
