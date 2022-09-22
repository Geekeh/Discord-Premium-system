from unittest import result
from discord.ext import commands
import discord
import time
import datetime
from pymongo import MongoClient

bot = commands.Bot(command_prefix=".", intents=discord.Intents.all())

#all your mongo db information
#mongo_db_link = 'Put your mongo db connection string'
#databases_name = 'Put your database name here' # -- Example https://ibb.co/1fpQktR
#collection_name = "Put your database collection name here" # -- Example https://ibb.co/Fwwvbxw

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
                        em = discord.Embed(color=0x852525)
                        em.add_field(name='Key expired', value=f'<@{user}> Your key is expired' + "\n" + "Key:" + key)
                        await ctx.send(embed=em)
                        collection.delete_many({"key": key})
                else:
                        pass


bot.run("discord bot token here")
