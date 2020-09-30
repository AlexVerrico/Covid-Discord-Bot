# Covid Discord Bot

This is a basic Discord bot to give you updates on covid 19. It currently has offical support for a limited number of countries, with more coming soon. Some other countries may work, but there is no guarantee. You can use the following link to add the bot to your server:
[https://discord.com/api/oauth2/authorize?client_id=757760561772626051&permissions=67584&scope=bot](https://discord.com/api/oauth2/authorize?client_id=757760561772626051&permissions=67584&scope=bot)

Supported locations:
* Australia
* USA
* All Australian States and Territories.

Available commands:

* `!covid new cases <location>`  
Displays the number of new cases for today and yesterday for the provided location
* `!covid new deaths <location>`  
Displays the number of new deaths for today and yesterday for the provided location
* `!covid new recoveries <location>`  
Displays the number of recoveries for today and yesterday for the given location.  
* `!covid graph`  
Displays a graph of new cases for all Australian States and Territories for the last 2 weeks

### If you find this Bot useful, please consider supporting my work through [BuyMeACoffee.com/AlexVerrico](https://www.buymeacoffee.com/AlexVerrico)

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
```  
For more info on how to get a discord bot token see [https://discordpy.readthedocs.io/en/latest/discord.html#discord-intro](https://discordpy.readthedocs.io/en/latest/discord.html#discord-intro)
You can replace the value of `PREFIX=` with any prefix that you want.  

If you find a bug to fix, or want to add a feature, please open an issue to discuss it first to avoid multiple people working on the same thing needlessly.  
Please ensure that all PRs are made to the `dev` branch  
Please ensure that you follow the style of the code (eg. spaces not tabs, function names use underscores, global variables use uppercase letters to seperate words (globalVariable), local variables are all lowercase with no seperation between words (localvariable)  
Please use descriptive function and variable names  
Please update any relevant documentation  

## PSAs:
 - ~~26/9/20: `!covid new recoveries <state>` is broken. Currently no ETA for repair.~~
    - Fixed 28/9/20 by @AlexVerrico
 
## Changelog:
 - 30/9/20: Added `!covid graph` command (@AlexVerrico)
## Contributors:
 - [@AlexVerrico](https://github.com/AlexVerrico/)
