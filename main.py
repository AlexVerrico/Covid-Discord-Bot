import os
import CovidParser
import datetime
from dotenv import load_dotenv
from discord.ext import commands
from matplotlib import pyplot as plt
import discord.file
import json
from discord import Embed as discord_Embed

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
PREFIX = os.getenv('PREFIX')
BASE = os.getenv('COVID_BOT_BASEDIR')

if os.getenv('COVID_BOT_LOGFILE2'):
    log_file = os.getenv('COVID_BOT_LOGFILE2')


    def log(data):
        with open(log_file, 'a') as f:
            f.write(f'{data}\n\n')
        return


    print = log

if os.getenv('COVID_BOT_LOGFILE1'):
    covid = CovidParser.CovidParser(cache_type=2, cache_update_interval=180, log_file=os.getenv('COVID_BOT_LOGFILE1'))
else:
    covid = CovidParser.CovidParser(cache_type=2, cache_update_interval=180, log_file=None)

bot = commands.Bot(command_prefix="".join((PREFIX, ' ')))

success_message = """Today: **{tday}**
Yesterday: **{yday}**
Source: *{source}*
*Built by [Alex Verrico](https://alexverrico.com/)*"""

location_not_supported_message = """Unfortunately, we don't support that location yet.
Please check that it was spelt correctly, and if so feel free to submit a request for it to be added:
https://github.com/AlexVerrico/Covid-Discord-Bot"""

data_type_not_supported_message = """Unfortunately, we don't support that data type yet.
Please check that it was spelt correctly, and if so feel free to submit a request for it to be added:
https://github.com/AlexVerrico/Covid-Discord-Bot"""

unknown_error_message = """Looks like we ran into an error. Please try again later, or get in touch and we can help:
https://alexverrico.com/#contact"""

average_message = """Last 14 days in {location}: **{data}**
*Built by [Alex Verrico](https://alexverrico.com/)*"""

total_message = """To date there have been **{data}** confirmed {data_type} of covid-19 recorded for {location}
*Built by [Alex Verrico](https://alexverrico.com/)*"""

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
    data = covid.new(location=loc, data_type=data_type, date_range={'type': 'days', 'value': 3}, include_date=False)
    print(data['content'])
    if data['status'] == 'error':
        if data['content'] == 'Unrecognised location':
            return discord_Embed(title='Error', description=location_not_supported_message, color=0xFF0000)
        elif data['content'] == 'Unsupported data_type':
            return discord_Embed(title='Error', description=data_type_not_supported_message, color=0xFF0000)
        else:
            return discord_Embed(title='Error', description=unknown_error_message, color=0xFF0000)
    elif data['status'] == 'ok':
        data = json.loads(data['content'])
        if int(data[0]) <= int(data[1]) and int(data[0]) < 50:
            color = 0x00FF00
        elif int(data[0]) < 50:
            color = 0xFF7F00
        else:
            color = 0xFF0000
        if loc in locationsv2 and loc != 'usa':
            response = discord_Embed(title='New {d_t} for {loc}'.format(loc=locationsv2[loc]['name'], d_t=data_type),
                                     description=success_message.format(tday=data[0], yday=data[1],
                                                                        source=locationsv2[loc]['source']),
                                     colour=color)
        elif loc == 'usa':
            response = discord_Embed(title='New {d_t} for {loc}'.format(loc=locationsv2[loc]['name'], d_t=data_type),
                                     description=success_message.format(tday=data[1], yday=data[2],
                                                                        source=locationsv2[loc]['source']),
                                     colour=color)
        else:
            response = discord_Embed(title='New {d_t} for {loc}'.format(loc=loc, d_t=data_type),
                                     description=success_message.format(tday=data[1], yday=data[2],
                                                                        source='epidemic-stats.com'),
                                     colour=color)
        return response
    else:
        return discord_Embed(title='Error', description=unknown_error_message, color=0xFF0000)


@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord at {datetime.datetime.now().strftime("%H:%M %d-%m-%y")}')
    return


@bot.command(name='new', help='Shows new data')
async def new(ctx, data_type='cases', location='aus'):
    response = get_data(location.lower(), data_type)
    await ctx.send(embed=response)
    return


@bot.command(name='graph', help='Displays a graph of cases in Australian states for the last 14 days')
async def graph(ctx):
    # dldata = covid._fetch_data_v3(r"https://atlas.jifo.co/api/connectors/0b334273-5661-4837-a639-e3a384d81d20")
    # dldata = json.loads(dldata)
    # dldata = dldata["data"]
    # dldata = dldata[8]
    dldata = []
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

    for location in data.keys():
        if location == 'dates':
            location = 'vic'
            index = 0
        else:
            index = 1
        _data = covid.new(location=location, data_type='cases',
                          include_date=True, date_range={'type': 'days', 'value': 14})
        if _data['status'] == 'error':
            if _data['content'] == 'Unrecognised location':
                return discord_Embed(title='Error', description=location_not_supported_message, color=0xFF0000)
            elif _data['content'] == 'Unsupported data_type':
                return discord_Embed(title='Error', description=data_type_not_supported_message, color=0xFF0000)
            else:
                return discord_Embed(title='Error', description=unknown_error_message, color=0xFF0000)
        elif _data['status'] == 'ok':
            out = []
            for x in json.loads(_data['content']):
                out.append(x[index])
            dldata.append(out)
        else:
            return discord_Embed(title='Error', description=unknown_error_message, color=0xFF0000)

    temp_vals = []

    for i in range(0, 14):
        for x in data:
            if x == "dates":
                data[x]['data'].insert(0, dldata[data[x]['num']][i])
            else:
                d = dldata[data[x]['num']][i]
                if d == '':
                    d = 0
                data[x]['data'].insert(0, int(d))

    fig = plt.figure(dpi=128, figsize=(10, 6))

    for i in data:
        if i == 'dates':
            continue
        else:
            plt.plot(data['dates']['data'], data[i]['data'], c=data[i]['color'], label=data[i]['label'])
            for x in data[i]['data']:
                temp_vals.append(int(x))
            for x, y in zip(data['dates']['data'], data[i]['data']):
                if y != 0:
                    plt.annotate(xy=[x, y], text=y, c=data[i]['color'])

    plt.title("Cases from last 2 weeks", fontsize=24)
    max_val = 0
    for i in temp_vals:
        if i > max_val:
            max_val = i
    max_val = max_val + int(max_val / 10)
    plt.ylim(0, max_val)
    plt.xlabel('Date', fontsize=16)
    plt.ylabel("Cases", fontsize=16)
    plt.tick_params(axis='both', which='major', labelsize=6)
    plt.legend()
    fig.savefig('graph.jpg')
    await ctx.send(file=discord.File('graph.jpg'))
    os.remove('graph.jpg')
    return


@bot.command(name='average', help='14 day average')
async def average(ctx, data_type='cases', location='aus'):
    data = covid.new(location=location, data_type=data_type, date_range={'type': 'days', 'value': 14})
    if data['status'] == 'error':
        if data['content'] == 'Unrecognised location':
            return discord_Embed(title='Error', description=location_not_supported_message, color=0xFF0000)
        elif data['content'] == 'Unsupported data_type':
            return discord_Embed(title='Error', description=data_type_not_supported_message, color=0xFF0000)
        else:
            return discord_Embed(title='Error', description=unknown_error_message, color=0xFF0000)
    elif data['status'] == 'ok':
        data = json.loads(data['content'])
        x = 0
        for i in range(0, 14):
            if data[i] == '':
                y = 0
            else:
                y = int(data[i])
            x = x + y
        x = float(x) / 14
        x = float(str(x)[:4])
        response = discord_Embed(title='Average {d_t} per day'.format(d_t=data_type),
                                 description=average_message.format(location=location, data=x))
        await ctx.send(embed=response)
    else:
        return discord_Embed(title='Error', description=unknown_error_message, color=0xFF0000)


@bot.command(name='total', help='Total covid-19 cases recorded to date')
async def total(ctx, data_type='cases', location='aus'):
    data = covid.total(data_type=data_type, location=location)
    if data['status'] == 'error':
        if data['content'] == 'Unrecognised location':
            return discord_Embed(title='Error', description=location_not_supported_message, color=0xFF0000)
        elif data['content'] == 'Unsupported data_type':
            return discord_Embed(title='Error', description=data_type_not_supported_message, color=0xFF0000)
        else:
            return discord_Embed(title='Error', description=unknown_error_message, color=0xFF0000)
    elif data['status'] == 'ok':
        response = discord_Embed(title='Total {d_t} for {loc}'.format(d_t=data_type, loc=location),
                                 description=total_message.format(
                                     location=location, data=data['content'], data_type=data_type)
                                 )
        await ctx.send(embed=response)
        return
    else:
        return discord_Embed(title='Error', description=unknown_error_message, color=0xFF0000)


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

    help_description = """**Commands:**"""

    new_field = """This command provides the number of new cases, recoveries, or deaths from the last 2 days, use it like
_**!covid new cases vic**_"""

    total_field = """This command provides the total number of cases, recoveries, or deaths recorded to date, use it like
_**!covid total deaths nsw**_"""

    graph_field = """This command provides a graph of the number of new cases per day for the last 14 days in each australian state, use it like
_**!covid graph**_"""

    average_field = """This command provides the average number of daily new cases, recoveries, or deaths from the last 14 days, use it like
_**!covid average recoveries aus**_"""

    more_info_field = """For more information, visit https://github.com/AlexVerrico/Covid-Discord-Bot/"""

    built_by_field = """You can support me by [donating](https://www.buymeacoffee.com/AlexVerrico) or [hiring me](https://alexverrico.com/#contact)."""

    response = discord_Embed(title='Covid AU Bot', description=help_description)
    response.add_field(name='!covid new', value=new_field, inline=False)
    response.add_field(name='!covid total', value=total_field, inline=False)
    response.add_field(name='!covid average', value=average_field, inline=False)
    response.add_field(name='!covid graph', value=graph_field, inline=False)
    response.add_field(name='More info:', value=more_info_field, inline=False)
    response.add_field(name='Built by Alex Verrico', value=built_by_field, inline=False)
    await ctx.send(embed=response)


if os.getenv('COVID_BOT_DO_POG'):
    @bot.event
    async def on_message(message):
        ctx = await bot.get_context(message)
        if str(message.content).startswith('!pog'):
            await ctx.send(file=discord.File("".join((BASE, 'imgs/pog.png'))))
        await bot.invoke(ctx)
        return

bot.run(TOKEN)
