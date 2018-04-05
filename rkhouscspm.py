import requests
import json
import subprocess
import os
import sys, traceback
import configparser
import MySQLdb
import discord
from discord.ext import commands
import asyncio
from pokemonlist import pokemon, pokejson
from config import bot_channel, token, host, user, password, database, website, log_channel, spawn_channel
from datetime import datetime
from datetime import timedelta
import calendar
import logging
from datetime import time
from datetime import date
import datetime
import random
## CREATED BY @rkhous#1447

logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

bot = commands.Bot(command_prefix = '^')#set prefix

database = MySQLdb.connect(host,user,password,database)
database.ping(True)
cursor = database.cursor()

@bot.event
async def on_ready():
    print()
    print()
    print("Login successful.")
    print("-----------------")
    print("CSPM by @rkhous#1447")
    print("-----------------")
    print("BotUser = "+str(bot.user))
    print("-----------------")
    print("-----started-----")
    print("The time is now")
    print(datetime.datetime.now())

def find_pokemon_id(name):
    if name == 'Nidoran-F':
        return 29
    elif name == 'Nidoran-M':
        return 32
    elif name == 'Mr-Mime':
        return 122
    elif name == 'Ho-Oh':
        return 250
    elif name == 'Mime-Jr':
        return 439
    else:
        name = name.split('-')[0]
        for k in pokejson.keys():
            v = pokejson[k]
            if v == name:
                return int(k)
        return 0

def find_pokecp(name):
    with open('pokecp.json') as f:
        data = json.load(f)
        return (data[str(name).capitalize()])

#raid function
@bot.command(pass_context=True)
async def raid(ctx, arg, arg2, arg3, arg4):#arg = gym name, arg2 = pokemon name, arg3 = level, arg4 = time remaining
    if ctx and ctx.message.channel.id == str(bot_channel) and str(arg2).lower() in pokemon:
        """example: ^raid "Canandagua National Bank Clock Tower" Lugia 5 45"""

        pokemon_id = find_pokemon_id(str(arg2).capitalize())
        pokecp = find_pokecp(str(arg2).capitalize())
        now = datetime.datetime.utcnow() + timedelta(minutes=int(arg4))
        time = datetime.datetime.utcnow() + timedelta()

        try:
            cursor.execute("SELECT gym_id FROM gymdetails WHERE name LIKE '" + str(arg) + "%';")
            gym_id = str(cursor.fetchall())
            gym_id = gym_id.split(',')
            gym_id = gym_id[0].split('((')
            cursor.execute("REPLACE INTO raid("
                           "gym_id, level, spawn, start, "
                           "end, pokemon_id, cp, move_1, "
                           "move_2, last_scanned)"
                           " VALUES ("+str('{}').format(gym_id[1])+", "+str(arg3)+", "+str("'{}'").format(time)+", "+str("'{}'").format(time)+", "+str("'{}'").format(now)+", "+str(pokemon_id)+", "+str(pokecp)+", 1, 1, "+str("'{}'").format(time)+");")
                           #"VALUES (%s, %s, "+str("'{}'").format(time)+", "+str("'{}'").format(time)+", "+str("'{}'").format(now)+", %s, %s, 1, 1, "+str("'{}'").format(time)+");", (str(gym_id[1]), str(pokemon_id), str(arg3), str(arg5)))
            cursor.execute("UPDATE gym SET last_modified = '"+str(time)+"', last_scanned = '"+str(time)+"' WHERE gym_id = "+str(gym_id[1])+";")
            database.ping(True)
            database.commit()
            await bot.say('Successfully added your raid to the live map.')
            await bot.send_message(discord.Object(id=log_channel), str(ctx.message.author.name) + ' said there was a ' + str(arg2) +
                                   ' raid going on at ' + str(arg)) and print(str(ctx.message.author.name) + ' said there was a ' + str(arg2) +
                                   ' raid going on at ' + str(arg))
            #await bot.say("VALUES ("+str('{}').format(gym_id[1])+", "+str(arg3)+", "+str("'{}'").format(time)+", "+str("'{}'").format(time)+", "+str("'{}'").format(now)+", "+str(pokemon_id)+", "+str(pokecp)+", 1, 1, "+str("'{}'").format(time)+");")
            #await bot.say("UPDATE gym SET last_modified = '"+str(time)+"', last_scanned = '"+str(time)+"' WHERE gym_id = "+str(gym_id[1])+";")

        except:
            #database.connect()
            database.rollback()
            await bot.say('Unsuccesful in database query, your raid was not added to the live map.')
            await bot.say("Could not find `{}` in my database. Please check your gym name. \nuse `^gym gym-name` to try and look it up".format(arg))
            await bot.say("VALUES ("+str('{}').format(gym_id[1])+", "+str(arg3)+", "+str("'{}'").format(time)+", "+str("'{}'").format(time)+", "+str("'{}'").format(now)+", "+str(pokemon_id)+", "+str(pokecp)+", 1, 1, "+str("'{}'").format(time)+");")
            await bot.say("UPDATE gym SET last_modified = '"+str(time)+"', last_scanned = '"+str(time)+"' WHERE gym_id = "+str(gym_id[1])+";")
            tb = traceback.print_exc(file=sys.stdout)
            print(tb)

@bot.command(pass_context=True)
async def spawn(ctx, arg, arg2, arg3):
    if ctx and ctx.message.channel.id == str(bot_channel) and arg in pokemon:
        pokemon_id = find_pokemon_id(str(arg).capitalize())
        time = datetime.datetime.utcnow() + timedelta(minutes=15)
        time2 = datetime.datetime.utcnow() + timedelta()
        number = random.randint(1,2000000001)
        try:
            cursor.execute("REPLACE INTO pokemon(encounter_id, spawnpoint_id, pokemon_id, latitude, longitude, disappear_time, individual_attack, individual_defense, individual_stamina, move_1, move_2, cp, cp_multiplier, weight, height, gender, costume, form, weather_boosted_condition, last_modified)"
                           "VALUES ("+str(number)+", "+str(number)+", "+str(pokemon_id)+", "+str(arg2)+", "+str(arg3)+", '"+str(time)+"', null, null, null, null, null, null, null, null, null, null, null, null, null, '"+str(time2)+"');")

            database.ping(True)
            database.commit()
            await bot.say('Successfully added your spawn to the live map.\n'
                          '*Pokemon timers are automatically given 15 minutes since the timer is unknown.*')
            #await bot.say("VALUES ("+str(number)+", "+str(number)+", "+str(pokemon_id)+", "+str(arg2)+", "+str(arg3)+", '"+str(time)+"', null, null, null, null, null, null, null, null, null, null, null, null, null, null);")
            await bot.send_message(discord.Object(id=log_channel), str(ctx.message.author.name) + ' said there was a wild ' + str(arg) +
                                   ' at these coordinates: ' + str(arg2) + ', ' + str(arg3))  and print(str(ctx.message.author.name) + ' said there was a wild ' + str(arg) +
                                   ' at these coordinates: ' + str(arg2) + ', ' + str(arg3))

            spawn_embed=discord.Embed(
                title='Click for directions!',
                url=("https://www.google.com/maps/?q=" + str(arg2) + "," + str(arg3)),
                description=('A wild ' + str(arg).capitalize() + ' is available!\n\n'
                                                                 '**Time Remaining:** ~15 minutes.\n'
                                                                 '**Spotted by:** ' + str(ctx.message.author.name) + '!'),
                color=3447003
            )
            spawn_embed.set_image(url="http://www.pokestadium.com/sprites/xy/" + str(arg).lower() + ".gif")
            await bot.send_message(discord.Object(id=spawn_channel), embed=spawn_embed)

        except:
            tb = traceback.print_exc(file=sys.stdout)
            print(tb)
            await bot.say("VALUES ("+str(number)+", "+str(number)+", "+str(pokemon_id)+", "+str(arg2)+", "+str(arg3)+", '"+str(time)+"', null, null, null, null, null, null, null, null, null, null, null, null, null, null);")
            await bot.say('Unsuccessful in database query, your reported spawn was not added to the live map.')


@bot.command(pass_context=True)
async def gym(ctx, arg):
    cursor.execute("SELECT name FROM gymdetails WHERE name LIKE '" + str(arg) + "%';")
    gym_name = str(cursor.fetchall())
    msg = "`{}`".format(gym_name)
    database.commit()
    await bot.say(msg)

@bot.command()
async def commands():
    await bot.say("```^gym <\'gymname\'> -- show gyms like name provided, also a way to know if they are in the db.\n       Example: ^gym \"Calvary Chapel Of The Finger Lakes\"\n\n"
                  "^raid -- input raid into database so that it shows on map for all to see\n\n"
                  "^example -- shows an example of an input\n\n"
                  "^spawn -- creates a spawn on map. timer set to 15 min as it is unknown\n     Example: ^spawn mew 42.947890 -77.338575\n\n"
                  "gym names must be in \"quotes\"\n"
                  "\n\n^raidcp <MON> -- shows the raid cp of specified mon```")

@bot.command()
async def example():
    await bot.say("```^raid \"Canandagua National Bank Clock Tower\" Lugia 5 45\n"
                  "'gym-name' poke-name level time-remaining```")

@bot.command()
async def raidcp(arg):
    with open('pokecp.json') as f:
        data = json.load(f)
        await bot.say(data[str(arg).capitalize()])

@bot.command()
async def version():
        res = requests.get('https://pgorelease.nianticlabs.com/plfe/version')
        await bot.say("```\nCurrently Forced API: " + (res.text) + "```")

@bot.command(pass_context=True)
async def test(ctx, arg):

    cursor.execute("SELECT gym_id FROM gymdetails WHERE name LIKE '" + str(arg) + "%';")
    gym_id = str(cursor.fetchone())
    gym_id = gym_id.split("'")
    gym_id = str(gym_id[1])

    cursor.execute("SELECT url FROM gymdetails WHERE gym_id LIKE '" + str(gym_id) + "%';")
    image = str(cursor.fetchall())
    image = image.split("'")
    image = str(image[1])

    cursor.execute("SELECT latitude FROM gym WHERE gym_id LIKE '" + str(gym_id) + "%';")
    lat = str(cursor.fetchall())
    lat = lat.split("(")
    lat = str(lat[1]).split("'")

    cursor.execute("SELECT longitude FROM gym WHERE gym_id LIKE '" + str(gym_id) + "%';")
    lon = str(cursor.fetchall())
    #lon = lon.split(",")
    #lon = str(lon[0])

    cursor.execute("SELECT name FROM gymdetails WHERE name LIKE '" + str(arg) + "%';")
    gym_title = str(cursor.fetchall())
    #gym_title = gym_title.split("'")
    gym_title = str(gym_title)
    #if '"' in gym_title:
    #    gym_title = gym_title[1].split('"')
    #elif "'" in gym_title:
    #    gym_title = gym_title[1].split("'")

    msg = "`{}\n{}\n{}\n{}\n{}`".format(gym_id, image, lat, lon, gym_title)
    await bot.say(msg)



bot.run(token)
