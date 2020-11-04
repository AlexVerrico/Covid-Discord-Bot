import os
import CovidParser.covid_parser as covid
import datetime
from dotenv import load_dotenv
from discord.ext import commands
from matplotlib import pyplot as plt
import discord.file
import json

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
PREFIX = os.getenv('PREFIX')
BASE = os.getenv('COVID_BOT_BASEDIR')

bot = commands.Bot(command_prefix="".join((PREFIX, ' ')))

supportedResponse = """New %data_type% for %location%:
Today: %tday%
Yesterday: %yday%
Source: %source%"""
# semiSupportedResponse = "We don't fully support this location, however we were still able to find the information that you wanted:\nNew %data_type%:\nToday: %tday%\nYesterday: %yday%"
unsupportedResponse = """Error: that location is not supported yet.
See https://alexverrico.com/projects/CovidDiscordBot for a full list of supported locations."""
unsupportedDataTypeResponse = """Error: that data type is not supported yet.
See https://alexverrico.com/projects/CovidDiscordBot for a full list of supported data types."""

averageResponse = "Average daily %data_type% for last 14 days in %location%: %data%"

# locations = {'aus': 'Australia',
#              'nsw': 'New South Wales',
#              'vic': 'Victoria',
#              'qld': 'Queensland',
#              'sa': 'South Australia',
#              'wa': 'Western Australia',
#              'tas': 'Tasmania',
#              'nt': 'Northern Territory',
#              'act': 'Australian Capital Territory',
#              'usa': 'United States of America'
#              }

# sources = {'aus': 'covid19data.com.au',
#            'nsw': 'covid19data.com.au',
#            'vic': 'covid19data.com.au',
#            'qld': 'covid19data.com.au',
#            'sa': 'covid19data.com.au',
#            'wa': 'covid19data.com.au',
#            'tas': 'covid19data.com.au',
#            'nt': 'covid19data.com.au',
#            'act': 'covid19data.com.au',
#            'usa': 'epidemic-stats.com'
#            }

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
            return unsupportedDataTypeResponse
        response = supportedResponse.replace('%location%', locationsv2[loc]['name'])
        response = response.replace('%source%', locationsv2[loc]['source'])
        response = response.replace('%data_type%', data_type)
        response = response.replace('%tday%', data[0])
        response = response.replace('%yday%', data[1])
    else:
        data = covid.new(location=loc, data_type=data_type)
        if data == "unsupportedLocation":
            return unsupportedResponse
        response = supportedResponse.replace('%tday%', data[0])
        response = response.replace('%data_type%', data_type)
        response = response.replace('%yday%', data[1])
        response = response.replace('%source%', 'epidemic-stats.com')
        response = response.replace('%location%', loc)
    return response


@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord at {datetime.datetime.now().strftime("%H:%M %d-%m-%y")}')
    return


@bot.command(name='new', help='Shows new data')
async def new(ctx, data_type='cases', location='aus'):
    response = get_data(location.lower(), data_type)
    await ctx.send(response)
    return


@bot.command(name='graph', help='Displays a graph of cases in Australian states for the last 14 days')
async def graph(ctx):
    dldata = covid.download_data(r"https://atlas.jifo.co/api/connectors/0b334273-5661-4837-a639-e3a384d81d20")
    dldata = json.loads(dldata)
    dldata = dldata["data"]
    dldata = dldata[8]

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
    await ctx.send(file=discord.File('temp.jpg'))
    os.remove('temp.jpg')
    return


@bot.command(name='pogvic', help='is covid pog in vic?')
async def pogvic(ctx):
    _tempcases = covid.new('vic', data_type='cases')
    _tempdeaths = covid.new('vic', data_type='deaths')
    if int(_tempdeaths[0]) < int(_tempdeaths[1]) or int(_tempdeaths[0]) == 0:
        if int(_tempcases[0]) < int(_tempcases[1]) or int(_tempcases[0]) == 0:
            await ctx.send('covid:', file=discord.File("".join((BASE, 'imgs/pog.png'))))
        else:
            await ctx.send('not pog')
    else:
        await ctx.send('not pog')
    return


@bot.command(name='pog', help='is covid pog in aus?')
async def pog(ctx):
    _tempcases = covid.new('aus', data_type='cases')
    _tempdeaths = covid.new('aus', data_type='deaths')
    if _tempdeaths[0] < _tempdeaths[1] or _tempdeaths[0] == "0":
        if _tempcases[0] < _tempcases[1] or _tempcases[0] == "0":
            await ctx.send('covid:', file=discord.File("".join((BASE, 'imgs/pog.png'))))
        else:
            await ctx.send('not pog')
    else:
        await ctx.send('not pog')
    return


@bot.command(name='average', help='14 day average')
async def average(ctx, data_type='cases', location='aus'):
    data = covid.new(location=location, data_type=data_type, time='14days')
    x = 0
    for i in range(0, 14):
        if data[i] == '':
            y = 0
        else:
            y = int(data[i])
        x = x + y
    x = float(x) / 14
    x = float(str(x)[:4])
    response = averageResponse.replace('%location%', location)
    response = response.replace('%data_type%', data_type)
    response = response.replace('%data%', str(x))
    await ctx.send(response)


@bot.command(name='total', help='Total covid-19 cases recorded to date')
async def total(ctx, data_type='cases', location='global'):
    data = covid.total(data_type='cases', location='global')
    response = f'To date there have been {data} confirmed cases of covid-19 recorded globally.'
    await ctx.send(response)
    return


bot.remove_command('help')


@bot.command(name='help')
async def helper(ctx):
    help_response = """
    **Covid AU Bot:**
_A simple discord bot to give you up-to-date info on Covid-19_
**Commands:**
**new**: Provides data for the last 2 days for the chosen location. Use it like `!covid new cases aus`
**graph**: Displays a graph of cases in Australian states for the last 14 days. Use it like `!covid graph`
**average**: Displays the 14 day average for the chosen location. Use it like `!covid average cases aus`
**total**: Total covid-19 cases recorded to-date. Use it like `!covid total`
**pog**: Is covid Pog in Australia? Use it like `!covid pog`
**pogvic**: Is covid Pog in Victoria? Use it like `!covid pogvic`

For more information, visit https://github.com/AlexVerrico/Covid-Discord-Bot/

_This bot also responds to `!pog`, I'll let you figure out what that does :wink:._

Developed by Alex Verrico (https://alexverrico.com/)
_If you find this bot useful, please consider supporting it through https://www.buymeacoffee.com/AlexVerrico_
"""
    await ctx.send(help_response)


@bot.event
async def on_message(message):
    ctx = await bot.get_context(message)
    if str(message.content).startswith('!pog'):
        await ctx.send(file=discord.File("".join((BASE, 'imgs/pog.png'))))
    if 'biden' in str(message.content):
        if str(ctx.author) != "Covid AU Testing Bot#2116":
            x = """||Fuck|| biden
||_Please note that this does not necessarily reflect the opinions of the bots creators :grin:_||"""
            await ctx.send(x)
    await bot.invoke(ctx)
    return


bot.run(TOKEN)
