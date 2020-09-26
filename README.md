# Covid Discord Bot

### PSA 26/9/20: `!covid new recoveries <state>` is broken. Currently no ETA for repair.

This is a basic Discord bot to give you updates on covid 19. It currently has offical support for a limited number of countries, with more coming soon. Some other countries may work, but there is no guarantee. You can use the following link to add the bot to your server:
[https://discord.com/api/oauth2/authorize?client_id=757760561772626051&permissions=67584&scope=bot](https://discord.com/api/oauth2/authorize?client_id=757760561772626051&permissions=67584&scope=bot)

Supported locations:
* Australia
* USA
* All Australian States and Territories.

Available commands:

* !covid new cases &lt;location&gt;  
Displays the number of new cases for today and yesterday for the provided location
* !covid new deaths &lt;location&gt;  
Displays the number of new deaths for today and yesterday for the provided location
* !covid new recoveries &lt;location&gt;  
Displays the number of recoveries for today and yesterday for the given location.


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
