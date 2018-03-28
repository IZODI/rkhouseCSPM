import configparser
import MySQLdb
import discord
from discord.ext import commands
import asyncio
from pokemonlist import pokemon, pokejson
from config import bot_channel, token, host, user, password, database, website, log_channel
import datetime
import calendar
import logging

logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

bot = commands.Bot(command_prefix = '^')#set prefix to .

database = MySQLdb.connect(host,user,password,database)

cursor = database.cursor()

@bot.event
async def on_ready():
    print("Login successful.")
    print("-----------------")
    print("CSPM by rkhous")
    print("-----------------")
    print(str(bot.user))
    print("-----------------")
    print("-----started-----")



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

def get_time(minute):
    future = datetime.datetime.utcnow() + datetime.timedelta(minutes=minute)
    return calendar.timegm(future.timetuple())

#raid function
@bot.command(pass_context=True)
async def raid(ctx, arg, arg2, arg3, arg4, arg5):#arg = gym name, arg2 = pokemon name, arg3 = level, arg4 = time remaining, arg5 = cp
    if ctx and ctx.message.channel.id == str(bot_channel) and str(arg2).lower() in pokemon:
        pokemon_id = find_pokemon_id(str(arg2).capitalize())
        time = get_time(int(arg4))
        try:
            cursor.execute("SELECT gym_id FROM gymdetails WHERE name LIKE '" + str(arg) + "%';")
            gym_id = str(cursor.fetchall())
            gym_id = gym_id.split(',')
            gym_id = gym_id[0].split('((')
            cursor.execute("INSERT INTO raid("
                           "gym_id, level, spawn, start, "
                           "end, pokemon_id, cp, move_1, "
                           "move_2, last_scanned)"
                           "VALUES " +(str(gym_id[1])), str(arg3), + "'2018-03-27 05:00:00.880807', '2018-03-27 05:00:00.880807'," + str(arg4), str(pokemon_id), str(arg5), 1, 1, + "'2018-03-27 05:00:00.880807');")
            database.commit()
            await bot.say('Successfully added your raid to the live map.')
            await bot.send_message(discord.Object(id=log_channel), str(ctx.message.author.name) + ' said there was a ' + str(arg2) +
                                   ' raid going on at ' + str(arg)) and print(str(ctx.message.author.name) + ' said there was a ' + str(arg2) +
                                   ' raid going on at ' + str(arg))
        except:
            database.rollback()
            await bot.say('Unsuccesful in database query, your raid was not added to the live map.')

bot.run(token)
