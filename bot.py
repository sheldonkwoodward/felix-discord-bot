import discord
import asyncio
import requests
import json

import auth
import channels

client = discord.Client()


@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')


@client.event
async def on_message(message):
    # we do not want the bot to reply to itself
    if message.author == client.user:
        return

    if message.content.startswith('!hello'):
        msg = 'Hello {0.author.mention}'.format(message)
        await client.send_message(message.channel, msg)


async def added_hourly():
    await client.wait_until_ready()
    channel = discord.Object(id=channels.new_releases)
    felix_url_base = 'http://localhost:8000/'
    headers = {'Authorization': 'Bearer {0}'.format(auth.felix_token)}

    felix_url = '{0}media/hours/1'.format(felix_url_base)

    while not client.is_closed:
        response = requests.get(felix_url, headers=headers)
        response = json.loads(response.content.decode('utf-8'))
        message = str()
        
        if response['movie_num'] > 0:
            message += '__**New Movies**__\n'
            for movie in response['movies']:
                message += movie['title'] + ' (' + str(movie['release_year']) + ')'
                if movie['resolution'] != '1080p':
                    message += ' - ' + movie['resolution'] + '\n'
                else:
                    message += '\n'
                    
        if response['season_num'] > 0:
            message += '__**New Seasons**__\n'
            for season in response['seasons']:
                message += season['title'] + ' Season ' + str(season['season']) + '\n'

        if response['episode_num'] > 0:
                    message += '__**New Episodes**__\n'
                    for episode in response['episodes']:
                        message += season['title'] + ' Season ' + str(season['season']) + ' Episode ' + str(season['episode']) + '\n'

        if response['movie_num'] > 0 or response['season_num'] > 0:
            await client.send_message(channel, message)
        print('added_hourly()')
        await asyncio.sleep(3600)


client.loop.create_task(added_hourly())
client.run(auth.discord_token)
