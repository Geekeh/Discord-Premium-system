from unittest import result
from discord.ext import commands
import discord
import time
import datetime
from pymongo import MongoClient

bot = commands.Bot(command_prefix=".", intents=discord.Intents.all())

#all your mongo db information
mongo_db_link = 'Put your mongo db connection string'
databases_name = 'Put your database name here' # -- Example https://ibb.co/1fpQktR
collection_name = "Put your database collection name here" # -- Example https://ibb.co/Fwwvbxw

#this is the channel where it will say key expired
channel_to_send_messages = (Replace this with your channel id)

@bot.command()
async def enable(ctx):
    print("Connecting...")
    while True:
        time.sleep(5)
        mongo_url = mongo_db_link
        cluster = MongoClient(mongo_url)
        db = cluster[databases_name]
        collection = db[collection_name]

        #search through entire db
        db_info = collection.find({})
        for db_info in db_info:
                #get all info needed to check user and key
                expiration = db_info['expiration']
                user = db_info['user']
                key = db_info['key']
                current_date = datetime.datetime.today()
                check_time = datetime.datetime.strptime(expiration, "%y-%m-%d")
                if current_date > check_time:
                        channel = bot.get_channel(channel_to_send_messages)
                        em = discord.Embed(color=0x852525)
                        em.add_field(name='Key expired', value=f'<@{user}> Your key is expired' + "\n" + "Key: " + key)
                        await channel.send(embed=em)
                        collection.delete_many({"key": key})
                else:
                        pass


bot.run("replace with your discord bot token)
