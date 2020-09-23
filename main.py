import os
import CovidParser.covid_parser as covid
import datetime
from dotenv import load_dotenv
from discord.ext import commands

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
PREFIX = os.getenv('PREFIX')

# client = discord.Client()

bot = commands.Bot(command_prefix="".join((PREFIX, ' ')))

supportedResponse = "New %data_type% for %location%:\nToday: %tday%\nYesterday: %yday%\nSource: %source%"
semiSupportedResponse = "We don't fully support this location, however we were still able to find the information that you wanted:\nNew %data_type%:\nToday: %tday%\nYesterday: %yday%"
unsupportedResponse = "Error: that location is not supported yet. See example.com for a full list of supported locations."

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
    if data_type == 'cases':
        if loc in locationsv2:
            data = covid.new_cases(location=loc)
            response = supportedResponse.replace('%location%', locationsv2[loc]['name'])
            response = response.replace('%source%', locationsv2[loc]['source'])
            response = response.replace('%data_type%', data_type)
            response = response.replace('%tday%', data[0])
            response = response.replace('%yday%', data[1])
        else:
            try:
                data = covid.new_cases(location=loc)
                response = semiSupportedResponse.replace('%tday%', data[0])
                response = response.replace('%data_type%', data_type)
                response = response.replace('%yday%', data[1])
            except:
                response = unsupportedResponse
        return response
    elif data_type == 'deaths':
        if loc in locationsv2:
            data = covid.new_deaths(location=loc)
            response = supportedResponse.replace('%location%', locationsv2[loc]['name'])
            response = response.replace('%source%', locationsv2[loc]['source'])
            response = response.replace('%data_type%', data_type)
            response = response.replace('%tday%', data[0])
            response = response.replace('%yday%', data[1])
        else:
            try:
                data = covid.new_deaths(location=loc)
                response = semiSupportedResponse.replace('%tday%', data[0])
                response = response.replace('%data_type%', data_type)
                response = response.replace('%yday%', data[1])
            except:
                response = unsupportedResponse
        return response


@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord at %s' % datetime.datetime.now().strftime('%M:%H %d-%m-%y'))
    return


@bot.event
async def on_guild_join(ctx):
    with open('serverCount.txt', 'r') as f:
        count = int(f.read())
    with open('serverCount.txt', 'w') as f:
        count = count + 1
        f.write(str(count))
    return


@bot.event
async def on_guild_remove(ctx):
    with open('serverCount.txt', 'r') as f:
        count = int(f.read())
    with open('serverCount.txt', 'w') as f:
        count = count - 1
        f.write(str(count))
    return


@bot.command(name='new', help='Shows new info, see https://alexverrico.com/projects/CovidDiscordBot/ for more info')
async def new(ctx, data_type='cases', location='aus'):
    response = get_data(location.lower(), data_type)
    await ctx.send(response)


bot.run(TOKEN)
