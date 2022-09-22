from discord.ext import commands
import random
import string
from datetime import datetime
from datetime import timedelta
import datetime
import discord
from pymongo import MongoClient


bot = commands.Bot(command_prefix=".", intents=discord.Intents.all())

#all your mongo db information
mongo_db_link = 'Put your mongo db connection string'
databases_name = 'Put your database name here' # -- Example https://ibb.co/1fpQktR
collection_name = "Put your database collection name here" # -- Example https://ibb.co/Fwwvbxw

#key information
role_name = "Buyer"
key_prefix = "Discord" # -- Example: Discord-byXjAI

@bot.command()
@commands.has_permissions(manage_roles=True)  
async def gen(ctx, amount, time):
   key_int = int(amount)
   amount = key_int
   key_amt = range(int(amount))
   time = int(time)

   # -- Connect to database n shit
   mongo_url = mongo_db_link
   cluster = MongoClient(mongo_url)
   db = cluster[f"{databases_name}"]
   collection = db[f"{collection_name}"]

   # -- Expiration
   now = datetime.datetime.today()
   future = now + timedelta(days=time)
   expires = future.strftime("%y-%m-%d")

   # -- Key
   key_yes = f"{key_prefix}-fkEPsG"
   if key_int == 1:
      letters = string.ascii_letters
      key = f"{key_prefix}-" + ''.join(random.choice(letters) for i in range(6))
   elif key_int < 1:
      em = discord.Embed(color=0xff0000)
      em.add_field(name="Invalid number", value="Key amount needs to be higher than 0")
      await ctx.send(embed=em)
      return 0
   elif key_int > 1:
      amount = key_int - 1
      key_number = 1
      key_amt = range(int(amount))
      for i in key_amt:
         letters = string.ascii_letters
         key = f"{key_prefix}-" + ''.join(random.choice(letters) for i in range(6))
         em = discord.Embed(color=0xff0000)
         em.add_field(name=f"Key: {key_number}", value=key)
         await ctx.send(embed=em)
         key_number += 1
         post = {"key": key, "expiration": expires, "user": "Empty", "used": 'unused'}
         collection.insert_one(post)
      key = f"{key_prefix}-" + ''.join(random.choice(letters) for i in range(6))
   
   # -- collection.delete_many({}) #deletes all the keys

   # -- Send all info to discord and database
   message = await ctx.send("Connecting...")
   try:
      if key_int == 1:
         key_yes = key
      else:
         key_yes = f'{key_prefix}-fkEPsG'
         pass

      #sends key info to database
      
      post = {"key": key, "expiration": expires, "user": "Empty", "used": 'unused'}
      collection.insert_one(post)

      #make our embed that sends when key is genned
      em = discord.Embed(color=0x00ff00)
      em.add_field(name="\n" + "discord", value="**Key generated!**" + "\n" +
         "key: " + key + "\n" + "Expires: " + str(time) + " days" +  "\n" + "\n"
         + "**Redeem Key**" + "\n" + f"Redeem the key by typing ```.redeem {key}```")
      await message.delete()
      await ctx.send(embed=em)
   except:
      em = discord.Embed(color=0xff0000)
      em.add_field(name="Api did not respond", value="Could not generate key")
      await ctx.send(content="", embed=em)

#redeem function
@bot.command()
async def redeem(ctx, key):
   mongo_url = mongo_db_link
   cluster = MongoClient(mongo_url)
   db = cluster[f"{databases_name}"]
   collection = db[f"{collection_name}"]
   try:
      results = collection.find({"key": key})
      for results in results:
         if results['key'] == str(key):
            collection.update_one({"key": key}, {"$set":{"user": ctx.author.id}})
            expiration = str(results['expiration'])
            used = str(results['used'])
            if used == 'used':
               em = discord.Embed(color=0xff0000)
               em.add_field(name="Key already used", value="the key you entered has already been used")
               await ctx.send(embed=em)
            elif used == 'unused':
               role = role_name
               user = ctx.message.author
               await user.add_roles(discord.utils.get(user.guild.roles, name=role))
               em = discord.Embed(title="discord", color=0x00ff00)
               em.add_field(name="Redeemed!", value="You have successfully redeemed the key"
               + "\n" + "\n" + f"Key will expire on {expiration}")
               await ctx.send(embed=em)
               collection.update_one({"key": key}, {"$set":{"used": 'used'}})
               return
               
         else:
            em = discord.Embed(title="discord", color=0xff0000)
            em.add_field(name="Invalid key", value="The key you entered was invalid.")
            await ctx.send(embed=em)
   except:
      pass

bot.run('Discord bot token here')
