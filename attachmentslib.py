def merge_attachments(data, request):
    try:
        attachments = data['attachments']

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

    except KeyError:
        pass

    return (request)
