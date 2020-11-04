import CovidData

import os
import math
import json

import discord
from discord.ext import commands

# Returns a list of all areas in lower case
def get_areas_array(data):
    areas = [""] * len(data["data"])

    for i in range(len(data["data"])):
        areas[i] = data["data"][i]["area"].lower()

    return areas


# Check if config file exists, if not create one.
if os.path.exists("./config.json") == False:
    configJsonTemplate = {"token": "token",
                          "prefix": "&covid", "areaType": "", "area": ""}

    with open("./config.json", "w+") as f:
        json.dump(configJsonTemplate, f)

# Get data from config file
with open('./config.json') as f:
    configData = json.load(f)

token = configData["token"]
prefix = configData["prefix"]
areaType = configData["areaType"]
area = configData["area"]

bot = commands.Bot(command_prefix=f"{prefix} ")

# Get all area data from API
nationAreaData = CovidData.get_data(CovidData.generate_url("nation", "", True))
nationAreas = get_areas_array(nationAreaData)
regionAreaData = CovidData.get_data(CovidData.generate_url("region", "", True))
regionAreas = get_areas_array(regionAreaData)
utlaAreaData = CovidData.get_data(CovidData.generate_url("utla", "", True))
utlaAreas = get_areas_array(utlaAreaData)
ltlaAreaData = CovidData.get_data(CovidData.generate_url("ltla", "", True))
ltlaAreas = get_areas_array(ltlaAreaData)

# Returns a list of all possible area for the specifed area type
@bot.command(description="Returns a list of all possible areas for the specifed area type.")
async def areas(ctx, areaType):
    areaData = {}
    areaString = ""
    areaStrings = []

    if areaType == "nation":
        areaData = nationAreaData
    elif areaType == "region":
        areaData = regionAreaData
    elif areaType == "utla":
        areaData = utlaAreaData
    elif areaType == "ltla":
        areaData = ltlaAreaData

    for i in range(len(areaData["data"])):
        # Discord only accepts embed fields of 1024 length so this gets around that by creating multiple fields
        if len(areaString + (areaData['data'][i]['area'] + "\n")) > 1024:
            areaStrings.append(areaString)
            areaString = areaData["data"][i]["area"] + "\n"
        else:
            areaString += areaData["data"][i]["area"] + "\n"

    areaStrings.append(areaString)

    embed = discord.Embed(title=f"{areaType.upper()} - AREAS", description="These are all the areas available for that area type.", color=0x000000)

    for string in areaStrings:
        embed.add_field(name="\u200b", value=string, inline=True)

    await ctx.send(embed=embed)

# Sets the area type and area for the bot to use.
@bot.command(description="Sets the area type and area for the bot to use.")
async def setarea(ctx, iareaType, *, iarea):
    areaTypes = ["nation", "region", "utla", "ltla"]

    iareaType = iareaType.lower()
    iarea = iarea.lower()

    # Checks validity of areaType an area
    if iareaType in areaTypes:
        iareaValid = False
        if iareaType == "nation":
            if iarea in nationAreas:
                print("Valid Nation Area")
                iareaValid = True
        elif iareaType == "region":
            if iarea in regionAreas:
                print("Valid Region Area")
                iareaValid = True
        elif iareaType == "utla":
            if iarea in utlaAreas:
                print("Valid UTLA Area")
                iareaValid = True
        elif iareaType == "ltla":
            if iarea in ltlaAreas:
                print("Valid LTLA Area")
                iareaValid = True
        else:
            iareaValid = False

    if iareaValid:
        # Update the area and areaType
        global area
        area = iarea
        global areaType
        areaType = iareaType

        # Update the values of areaType and area in the config file
        with open("./config.json", "r+") as f:
            data = json.load(f)
            data["areaType"] = areaType
            data["area"] = area
            f.seek(0)
            f.write(json.dumps(data))
            f.truncate()

        await ctx.send(f"Set area type to {areaType} and area to {area}.")
    else:
        await ctx.send("Invalid Area.")

# Gets daily stats
@bot.command(description="Gets daily stats")
async def daily(ctx):
    dailyData = CovidData.get_data(CovidData.generate_url(areaType, area, "", True))

    await ctx.send(f"""```
    {area.upper()} - COVID STATS

    DAILY:
    - Data Date: {dailyData["data"][0]['date']}
    - New Cases: {dailyData["data"][0]['newCases']}```""")

# Gets weekly stats
@bot.command(description="Gets weekly stats")
async def weekly(ctx):
    sevenDayData = CovidData.get_data(CovidData.generate_url(areaType, area, "", "", True))

    await ctx.send(f"""```
    {area.upper()} - COVID STATS

    PAST 7 DAYS:
    - Data Date: {sevenDayData["data"][0]['date']}
    - Cases: {sevenDayData["data"][0]['newCases']}
    - Rate: {sevenDayData["data"][0]['rate']}```""")

# Gets all stats
@bot.command(description="Gets all stats")
async def stats(ctx):
    dailyData = CovidData.get_data(CovidData.generate_url(areaType, area, "", True))
    sevenDayData = CovidData.get_data(CovidData.generate_url(areaType, area, "", "", True))

    await ctx.send(f"""```
    {area.upper()} - COVID STATS
    
    OVERVIEW:
    - Total Cases: {dailyData["data"][0]['totalCases']}
    - Daily Data Date: {dailyData["data"][0]['date']}
    - Weekly Data Date: {sevenDayData["data"][0]['date']}

    DAILY:
    - New Cases: {dailyData["data"][0]['newCases']}

    PAST 7 DAYS:
    - Cases: {sevenDayData["data"][0]['newCases']}
    - Rate: {sevenDayData["data"][0]['rate']}```""")

bot.run(token)