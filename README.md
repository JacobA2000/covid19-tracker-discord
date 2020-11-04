[UK Government Coronavirus API]: https://coronavirus.data.gov.uk/developers-guide

# Discord Covid-19 Tracker
<img src="assets/Logo.png"  width="50" height="50"> 

A discord bot to track covid stats in the uk via the [UK Government Coronavirus API]

On the first run the bot will not boot, and instead a config.json file is created in the same directory as the bots main file. It will look similar to this:
```json 
{"token": "token", "prefix": "&covid", "areaType": "", "area": ""}
``` 
**You need to change the token value to your discord applications API token**   
*(You can also update the other values but it isn't required, and area and areaType can be set dynamically via bot commands.)*

**COMMANDS**  
*(To initiate a command type the prefix followed by the command and any parameters.)*
```
areas <areaType> - gets a list of valid areas for the specified area.
setarea <areaType> <area> - sets the areaType and area and updates the config file.
daily - gets the latest stats from the api.
weekly - gets the latest cumulative stats from the api.
stats - gets an overview of all included stats.
```

**EXAMPLES OF EXPECTED OUTPUT:**  
*Areas Command:*  
![areas command](/assets/areas_command.png?raw=true)

*Setarea Command:*  
![setarea command](/assets/setarea_command.png?raw=true)

*Daily Command:*  
![daily command](/assets/daily_command.png?raw=true)

*Weekly Command:*  
![weekly command](/assets/weekly_command.png?raw=true)

*Stats Command:*  
![stats command](/assets/stats_command.png?raw=true)
