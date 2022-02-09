import cloudscraper
import time
import discord
import re

#Discord bot token here
TOKEN = "OTM5NDEwNzM3MzgwNjIyMzk3.Yf4cbQ._FAAmdi9CHmm8MMGg-yL668qN_0"

client = discord.Client()

def get_id(name, timeout = 0):
    if timeout == 6:
        raise Exception("cloudflare")

    scraper = cloudscraper.create_scraper(
        delay=10, 
        interpreter='nodejs',
        browser={
            'browser': 'firefox',
            'platform': 'windows',
            'desktop': True,
            'mobile': False,
        }
    )
    collections = scraper.get("https://api-mainnet.magiceden.io/launchpad_collections")
    
    if"checking your browser" in collections.text:
        print("Failed")
        time.sleep(1)
        timeout += 1
        return get_id(name, timeout)
    else:
        for x in collections.json():
            if x["symbol"] == name:
                if "mint" in x:
                    return x["mint"]["candyMachineId"]
                else:
                    raise Exception("no_id")
            
def get_name(msg):
    regex = r"magiceden\.io/launchpad/([a-zA-Z0-9-_]+)"
    name = re.findall(regex,msg)
    if name != []:
        return name[0]
    else:
        return None

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if message.content.casefold().startswith("!cm"):
        name = get_name(message.content)
        print(name)
        try:
            ide = get_id(name)
        except Exception as e:
            if e.args[0] == "no_id":
                await message.channel.send("Candy Machine is not loaded, try again closer to launch date.")
            elif e.args[0] == "cloudflare":
                await message.channel.send("Failed to grab ID and bypass Cloudflare. Rotate browser dictionary values and interpreter.")
        else:
            await message.channel.send (f"**{name}:**")
            await message.channel.send(f"{ide}")
client.run(TOKEN)

(string.capitalize())