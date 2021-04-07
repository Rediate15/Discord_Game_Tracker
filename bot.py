import discord
from discord.utils import get
from discord.ext import commands, tasks
from game_scraper import Gamescraper
from errors import *
import sqlite3
from datetime import date
import traceback
import logging

logging.basicConfig(filename='tracker.log', format='%(asctime)s %(levelname)-8s %(message)s', level=logging.ERROR, datefmt='%Y-%m-%d %H:%M:%S')

conn = sqlite3.connect('gametracker.db')
#conn = sqlite3.connect(':memory:')
c = conn.cursor()

try:
    c.execute("""CREATE TABLE tracker (
        userId text,
        subId text,
        name text,
        url text,
        lastPrice text
                                        )""")
    conn.commit()
except:
    pass


def read_token():
    with open("token.txt", "r") as f:
        lines = f.readlines()
        return lines[0].strip()

token = read_token()

client = commands.Bot(command_prefix='::')
controleChannel = 705767412481654846
channelIds = [
                705767412481654846

            ]



@client.event
async def on_ready():
    checkprices.start()
    print(f'Logged in as {client.user.name}')

def is_controleChannel(ctx):
    return ctx.channel.id in channelIds

def log_error(tb):
    marker = "\n--------------------------------------------------------\n"
    logging.error(marker+": "+str(tb)+marker)

@client.event
@commands.check(is_controleChannel)
async def on_command_error(ctx, error):
    if isinstance(error, commands.errors.CommandNotFound):
        await ctx.send("Invalid command")
    if isinstance(error.original, InputError):
        await ctx.send("Wrong Input or Site could not be reached")
    if isinstance(error.original, NoGameError):
        await ctx.send("Couldn't find Game")
    if isinstance(error.original, FindPriceError):
        await ctx.send("Couldn't find Price")
    if isinstance(error.original, AlreadyTrackedError):
        await ctx.send("You already track this Game")
    else:
        tb = traceback.format_exception(type(error), error, error.__traceback__)
        log_error(tb)

@client.command(pass_context=True)
@commands.check(is_controleChannel)
async def info(ctx):
    messageBlock = discord.Embed()
    messageBlock.add_field(name=' ::info', value='Liste aller befehle', inline=False)
    messageBlock.add_field(name=' ::clean', value='Löscht Nachrichten im Channel', inline=False)
    messageBlock.add_field(name=' ::track Beispiel Spiel oder DLC kaufen http://www.beispiellink.de', value='Trackt das mit Namen angegebene Spiel unter der angegebenen Seite', inline=False)
    messageBlock.add_field(name=' ::track http://www.beispiellink.de', value='Trackt das erste Spiel auf dieser Seite', inline=False)
    messageBlock.add_field(name=' Bisher nur Support für:', value='Steam Spiel, DLCs und Bundels')
    messageBlock.add_field(name=' ::trackedGames', value='Zeigt alle von dir verfolgten Spiel', inline=False)
    messageBlock.add_field(name=' ::stopTracking Beispiel Spiel oder DLC kaufen', value='Entfernt das mit Namen angegebene Spiel von den von dir verfolgten Spielen', inline=False)
    messageBlock.add_field(name='Anmerkung:', value='Der Bot sollte für jeden täglich eine Meldung in diesen Channel senden, wenn der Preis eines verfolgten Spiels gesunken ist.\n Geplant ist, dass er dies in der Zukunft per Direktnachricht tut. Aus Überwachungsgründen ist diese Funktion noch ausgestellt', inline=False)
    messageBlock.add_field(name='Bugreport:', value='https://github.com/Rediate15/Discord_Game_Tracker/issues\n Unter diesem Link können Fehler gemeldet werden.\n Auch Vorschläge für neue Features können hier vorgeschlagen werden', inline=False)
    await ctx.send(embed=messageBlock)


@client.command(pass_context=True)
@commands.check(is_controleChannel)
async def clean(ctx):
    channel = ctx.channel
    count = 0
    async for _ in channel.history(limit=None):
        count += 1
    await ctx.channel.purge(limit=count-1)

@tasks.loop(seconds=20)
async def checkprices():
    c.execute('SELECT DISTINCT subId, url FROM tracker')
    subId_url_list = c.fetchall()
    if len(subId_url_list) == 0:
        return
    currentPrice_dict = {}
    for game in subId_url_list:
        currentPrice_dict[game[0]] = Gamescraper.getPrice(game[1], game[0])
    await sendNotificationChannelMessage(currentPrice_dict)
    

async def sendNotificationChannelMessage(currentPrice_dict):
    channel = client.get_channel(controleChannel)
    c.execute('SELECT DISTINCT userId FROM tracker')
    all_users = c.fetchall()
    for userId in all_users:
        try:
            c.execute('SELECT DISTINCT subId, name, url, lastPrice FROM tracker WHERE userId=:userId', {'userId': userId[0]})
            all_games_by_user = c.fetchall()
            user_object = await client.fetch_user(int(userId[0]))
            messageBlock = discord.Embed(title=str(date.today())+" Better Prices are available for:", description=user_object.mention, color=0x000000)
            counter = 0
            for entry in all_games_by_user:
                try:
                    entry_price_as_float = Gamescraper.convertPriceToFloat(entry[3])
                    current_price_as_float = Gamescraper.convertPriceToFloat(currentPrice_dict[entry[0]])
                    if entry_price_as_float != current_price_as_float:
                        if current_price_as_float < entry_price_as_float:
                            messageBlock.add_field(name=entry[1], value="Old Price: "+entry[3]+", New Price: "+currentPrice_dict[entry[0]]+"\n"+entry[2], inline=False)
                            counter += 1
                        with conn:
                            c.execute("""UPDATE tracker SET lastPrice = :lastPrice WHERE userId = :userId AND subId = :subId""", {'lastPrice': currentPrice_dict[entry[0]], 'userId': userId[0], 'subId': entry[0]})        
                except Exception as error:
                    tb = traceback.format_exception(type(error), error, error.__traceback__)
                    log_error(tb)
            if counter != 0:
                await channel.send(embed=messageBlock)
                #await client.send(user_object, embed=messageBlock)
        except Exception as error:
                    tb = traceback.format_exception(type(error), error, error.__traceback__)
                    log_error(tb)


@client.command(pass_context=True)
@commands.check(is_controleChannel)
async def stopTrack(ctx, *context):
    name = " ".join(context)
    deleted_entry = []
    with conn:
        c.execute("SELECT DISTINCT * FROM tracker WHERE userId=:userId AND name=:name", {'userId': str(ctx.message.author.id), 'name': name})
        deleted_entry = c.fetchall()
        c.execute("DELETE FROM tracker WHERE userId = :userId AND name = :name", {'userId': str(ctx.message.author.id) , 'name': name})
    if len(deleted_entry) == 0:
        await ctx.send("No such Game is being tracked")
    else:
        messageBlock = discord.Embed(title="Stoped tracking Game", color=0xFF0000)
        messageBlock.add_field(name=deleted_entry[0][2], value=deleted_entry[0][3], inline=False)
        messageBlock.add_field(name="Current Price", value=deleted_entry[0][4], inline=False)
        await ctx.send(embed=messageBlock)


@client.command(pass_context=True)
@commands.check(is_controleChannel)
async def stopAll(ctx):
    deleted_entry = []
    with conn:
        c.execute("SELECT DISTINCT * FROM tracker WHERE userId=:userId", {'userId': str(ctx.message.author.id)})
        deleted_entry = c.fetchall()
        c.execute("DELETE FROM tracker WHERE userId = :userId", {'userId': str(ctx.message.author.id)})
    if len(deleted_entry) == 0:
        await ctx.send("No game was being tracked")
    else:
        messageBlock = discord.Embed(title="Stoped tracking Games", color=0xFF0000)
        for entry in deleted_entry:
            messageBlock.add_field(name=entry[2], value=entry[3], inline=False)
            messageBlock.add_field(name="Current Price", value=entry[4], inline=False)
        await ctx.send(embed=messageBlock)


@client.command(pass_context=True)
@commands.check(is_controleChannel)
async def track(ctx, *context):
    url, subId, name = Gamescraper.compressEntry(" ".join(context))
    price = Gamescraper.getPrice(url, subId)           
    insertEntry(str(ctx.message.author.id) ,subId, name, url, price)
    messageBlock = discord.Embed(title="Game is being tracked", color=0x00FF00)
    messageBlock.add_field(name=name, value=url, inline=False)
    messageBlock.add_field(name="Current Price", value=price, inline=False)
    await ctx.send(embed=messageBlock)


@client.command(pass_context=True)
@commands.check(is_controleChannel)
async def trackedGames(ctx):
    listOfTrackedGames = selectUser(str(ctx.message.author.id))
    messageBlock = discord.Embed(title="Your tracked Games:", color=0x0000FF)
    for game in listOfTrackedGames:
        messageBlock.add_field(name=game[2], value=game[3]+"\n Current Price: "+Gamescraper.getPrice(game[3], game[1]), inline=False)
    await ctx.send(embed=messageBlock)

def selectUser(userId):
    c.execute('SELECT * FROM tracker WHERE userId=:userId', {'userId': userId})
    return c.fetchall()


@client.command(pass_context=True)
@commands.check(is_controleChannel)
async def testprice(ctx, *context):
    url, subId, name = Gamescraper.compressEntry(" ".join(context))
    price = Gamescraper.getPrice(url, subId)
    await ctx.send("Price for: "+name+"\n"+price)

def insertEntry(userId, subId, name, url, lastPrice):
    with conn:
        c.execute('SELECT * FROM tracker WHERE userId=:userId AND subId=:subId' , {'userId': userId, 'subId': subId})
        if len(c.fetchall()) != 0:
            raise AlreadyTrackedError(userId, subId)
        c.execute('INSERT INTO tracker VALUES (:userId, :subId, :name, :url, :lastPrice)', {'userId': userId, 'subId': subId, 'name': name, 'url': url, 'lastPrice': lastPrice})


client.run(token)
conn.close()