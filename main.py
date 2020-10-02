import os
import CovidParser.covid_parser as covid
import datetime
from dotenv import load_dotenv
from discord.ext import commands
import csv
from matplotlib import pyplot as plt
import discord.file
import json

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
PREFIX = os.getenv('PREFIX')

# client = discord.Client()

bot = commands.Bot(command_prefix="".join((PREFIX, ' ')))

supportedResponse = "New %data_type% for %location%:\nToday: %tday%\nYesterday: %yday%\nSource: %source%"
semiSupportedResponse = "We don't fully support this location, however we were still able to find the information that you wanted:\nNew %data_type%:\nToday: %tday%\nYesterday: %yday%"
unsupportedResponse = "Error: that location is not supported yet. See https://alexverrico.com/projects/CovidDiscordBot for a full list of supported locations."

locations = {'aus': 'Australia',
             'nsw': 'New South Wales',
             'vic': 'Victoria',
             'qld': 'Queensland',
             'sa': 'South Australia',
             'wa': 'Western Australia',
             'tas': 'Tasmania',
             'nt': 'Northern Territory',
             'act': 'Australian Capital Territory',
             'usa': 'United States of America'
             }

sources = {'aus': 'covid19data.com.au',
           'nsw': 'covid19data.com.au',
           'vic': 'covid19data.com.au',
           'qld': 'covid19data.com.au',
           'sa': 'covid19data.com.au',
           'wa': 'covid19data.com.au',
           'tas': 'covid19data.com.au',
           'nt': 'covid19data.com.au',
           'act': 'covid19data.com.au',
           'usa': 'epidemic-stats.com'
           }

locationsv2 = {
    'aus': {'name': 'Australia', 'source': 'covid19data.com.au'},
    'nsw': {'name': 'New South Wales', 'source': 'covid19data.com.au'},
    'vic': {'name': 'Victoria', 'source': 'covid19data.com.au'},
    'qld': {'name': 'Queensland', 'source': 'covid19data.com.au'},
    'sa': {'name': 'South Australia', 'source': 'covid19data.com.au'},
    'wa': {'name': 'Western Australia', 'source': 'covid19data.com.au'},
    'tas': {'name': 'Tasmania', 'source': 'covid19data.com.au'},
    'nt': {'name': 'Northern Territory', 'source': 'covid19data.com.au'},
    'act': {'name': 'Australian Capital Territory', 'source': 'covid19data.com.au'},
    'usa': {'name': 'United States Of America', 'source': 'epidemic-stats.com'}
}


def get_data(loc='aus', data_type='cases'):
    if loc in locationsv2:
        data = covid.new(location=loc, data_type=data_type)
        if data == "unsupportedDataType":
            return unsupportedResponse
        response = supportedResponse.replace('%location%', locationsv2[loc]['name'])
        response = response.replace('%source%', locationsv2[loc]['source'])
        response = response.replace('%data_type%', data_type)
        response = response.replace('%tday%', data[0])
        response = response.replace('%yday%', data[1])
    else:
        # try:
        data = covid.new(location=loc, data_type=data_type)
        if data == "unsupportedLocation":
            return unsupportedResponse
        response = semiSupportedResponse.replace('%tday%', data[0])
        response = response.replace('%data_type%', data_type)
        response = response.replace('%yday%', data[1])
        # except:
        #     response = unsupportedResponse
    return response


@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord at %s' % datetime.datetime.now().strftime('%M:%H %d-%m-%y'))
    return


# @bot.event
# async def on_guild_join(ctx):
#     with open('serverCount.txt', 'r') as f:
#         count = int(f.read())
#     with open('serverCount.txt', 'w') as f:
#         count = count + 1
#         f.write(str(count))
#     return
#
#
# @bot.event
# async def on_guild_remove(ctx):
#     with open('serverCount.txt', 'r') as f:
#         count = int(f.read())
#     with open('serverCount.txt', 'w') as f:
#         count = count - 1
#         f.write(str(count))
#     return


@bot.command(name='new', help='Shows new info, see https://alexverrico.com/projects/CovidDiscordBot/ for more info')
async def new(ctx, data_type='cases', location='aus'):
    response = get_data(location.lower(), data_type)
    await ctx.send(response)


@bot.command(name='botnew', help='Shows new info, see https://alexverrico.com/projects/CovidDiscordBot/ for more info')
@commands.has_role('Bots')
async def new(ctx, data_type='cases', location='aus'):
    response = get_data(location.lower(), data_type)
    await ctx.send(response)


@bot.command(name='graph')
async def graph(ctx):
    dldata = covid.download_data(r"https://atlas.jifo.co/api/connectors/0b334273-5661-4837-a639-e3a384d81d20")
    dldata = json.loads(dldata)
    dldata = dldata["data"]
    dldata = dldata[8]

    # filename = 'states14day.csv'

    data = {'dates': {'data': [], 'num': 0},
            'nsw': {'data': [], 'num': 1, 'color': 'black', 'label': 'NSW'},
            'vic': {'data': [], 'num': 2, 'color': 'blue', 'label': 'VIC'},
            'qld': {'data': [], 'num': 3, 'color': 'orange', 'label': 'QLD'},
            'sa': {'data': [], 'num': 4, 'color': 'green', 'label': 'SA'},
            'wa': {'data': [], 'num': 5, 'color': 'pink', 'label': 'WA'},
            'tas': {'data': [], 'num': 6, 'color': 'purple', 'label': 'TAS'},
            'nt': {'data': [], 'num': 7, 'color': 'red', 'label': 'NT'},
            'act': {'data': [], 'num': 8, 'color': 'grey', 'label': 'ACT'}
            }

    for i in range(1, 15):
        for x in data:
            if x == "dates":
                data[x]['data'].insert(0, dldata[-i][data[x]['num']])
            else:
                d = dldata[-i][data[x]['num']]
                if d == '':
                    d = 0
                data[x]['data'].insert(0, int(d))

    fig = plt.figure(dpi=128, figsize=(10, 6))

    for i in data:
        if i == 'dates':
            continue
        else:
            plt.plot(data['dates']['data'], data[i]['data'], c=data[i]['color'], label=data[i]['label'])
            for x, y in zip(data['dates']['data'], data[i]['data']):
                if y != 0:
                    plt.annotate(xy=[x, y], text=y, c=data[i]['color'])

    plt.title("Cases from last 2 weeks", fontsize=24)
    plt.ylim(0, 50)
    plt.xlabel('Date', fontsize=16)
    plt.ylabel("Cases", fontsize=16)
    plt.tick_params(axis='both', which='major', labelsize=6)
    plt.legend()
    fig.savefig('temp.jpg')
    # plt.show()
    await ctx.send(file=discord.File('temp.jpg'))
    os.remove('temp.jpg')


bot.run(TOKEN)
