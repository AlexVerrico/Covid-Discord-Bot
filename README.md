# Covid Discord Bot

This is a basic Discord bot to give you updates on Covid-19. It currently has offical support for a limited number of countries, with more coming soon. Some other countries may work, but there is no guarantee. You can use the following link to add the bot to your server:
[https://discord.com/api/oauth2/authorize?client_id=757760561772626051&permissions=378944&scope=bot](https://discord.com/api/oauth2/authorize?client_id=757760561772626051&permissions=378944&scope=bot)

**Currently supported locations:**  
_location (full name)_
- aus (Australia)
- nsw (New South Wales)
- vic (Victoria)
- qld (Queensland)
- sa (South Australia)
- wa (Western Australia)
- tas (Tasmania)
- nt (Northern Territory)
- act (Australian Capital Territory)
- usa (United States of America)

Any other location supported by [https://epidemic-stats.com/coronavirus/country_name](https://epidemic-stats.com/coronavirus/country_name) _should_ work, but is not a guarantee.

Unless otherwise stated, `<type>` can be cases, recoveries, or deaths.

Available commands:

* `!covid new <type> <location>`  
   Displays the number of new <type> for today and yesterday for the provided location. use it like `!covid new cases aus`
* `!covid total <type> <location>`  
  Total covid-19 <type> recorded to-date for <location>. Use it like `!covid total cases vic`  
* `!covid graph`  
  Displays a graph of new cases for all Australian States and Territories for the last 2 weeks. Use it like `!covid graph`
* `!covid average <type> <location`  
  Displays the 14 day average for the chosen location. Use it like `!covid average cases aus`
  
### If you find this Bot useful, please consider supporting my work by [donating](https://www.buymeacoffee.com/AlexVerrico) or [hiring me](https://alexverrico.com/#contact).  

## Contributing:

#### Setting up the environment:
Clone the repo using `git clone https://github.com/AlexVerrico/Covid-Discord-Bot.git`  
CD into the repo `cd Covid-Discord-Bot`  
Add the submodules using `git submodule init && git submodule update`  
You will need to install the python modules `discord.py`, `dotenv` and `urllib3`  
You will also need to create a file in your home directory named `.env` with the contents:  
```
DISCORD_TOKEN=[your-discord-bot-token]
PREFIX=!covid
COVID_BOT_BASEDIR=/path/to/bot/files/
COVID_BOT_LOGFILE1=/path/to/CovidParser_log.txt
COVID_BOT_LOGFILE2=/path/to/bot_log.txt
COVID_BOT_DO_POG=True
```
For more info on how to get a discord bot token see [https://discordpy.readthedocs.io/en/latest/discord.html#discord-intro](https://discordpy.readthedocs.io/en/latest/discord.html#discord-intro)
You can replace the value of `PREFIX=` with any prefix that you want.  
You can remove `COVID_BOT_DO_POG` to disable keyword detection for `!pog`

If you find a bug to fix, or want to add a feature, please open an issue to discuss it first to avoid multiple people working on the same thing needlessly.  
Please ensure that all PRs are made to the `dev` branch  
Please ensure that you follow the style of the code (eg. spaces not tabs, function names use underscores, global variables use uppercase letters to seperate words (globalVariable), local variables are all lowercase with no seperation between words (localvariable)  
Please use descriptive function and variable names  
Please update any relevant documentation  

## PSAs:
 - ~~26/9/20: `!covid new recoveries <state>` is broken. Currently no ETA for repair.~~  
    - Fixed 28/9/20 by @AlexVerrico  
 - ~~10/07/2021: `!covid total` is broken. Currently no ETA for repair.~~  
    - Fixed 22/7/21 by @AlexVerrico  
 
## Changelog:  
 - 30/9/20: Added `!covid graph` command (@AlexVerrico)  
 - Some time during October 2020: Added `!covid total`, `!covid pog`, `!covid pogvic`, `!covid average` (@AlexVerrico)  
 - 22/7/21: Version 2! Switches to Embeds for displaying most data, and during testing has proven to be more reliable.  

## Contributors:
 - [@AlexVerrico](https://github.com/AlexVerrico/)
