import datetime
from dotenv import load_dotenv
from discord.ext import tasks, commands
import discord
from bot import mongo, rss
import os

load_dotenv(verbose=True)

# Discord Variables
TOKEN = os.environ.get("TOKEN")
COMMAND_PREFIX = os.environ.get("COMMAND_PREFIX")
CRAWL_INTERVAL_MINUTES = int(os.environ.get("CRAWL_INTERVAL_MINUTES"))

bot = commands.Bot(command_prefix=COMMAND_PREFIX)


def get_channel(channel_id: int):
    channel = bot.get_channel(channel_id)
    if channel is None:
        mongo.delete_channel_subscriptions(channel_id)
    return channel


async def exec(url: str):
    feeds = rss.get_feeds(url)
    channels = [get_channel(channel_id) for channel_id in mongo.get_channel_ids(url)]
    for (title, url) in feeds:
        if mongo.feed(title, url):
            for channel in channels:
                if channel is None:
                    continue
                await channel.send(url)


def log(message: str):
    print(f"[{datetime.datetime.today()}] {message}")


@tasks.loop(minutes=CRAWL_INTERVAL_MINUTES)
async def loop():
    for url in mongo.get_all_subscription_urls():
        log(f"Start crawl {url}")
        await exec(url)
    log("Crawl completed.")


@bot.event
async def on_ready():
    log("Ready to crawl")
    loop.start()


@bot.command()
async def subscribe(context: commands.Context, url: str):
    title = rss.get_title(url)
    if title is None:
        await context.send(f"Invalid URL: {url}")
    else:
        mongo.subscribe(context.channel.id, title, url)
        await context.send(f"Success")
    result = "failed" if title is None else "succeeded"
    log(f"Subscribe command {result}. (USER ID: {context.author.id},URL: {url})")


@bot.command(name="subscriptions")
async def get_subscriptions(context: commands.Context):
    subscriptions = [f"{s[mongo.TITLE]}({s[mongo.URL]})" for s in mongo.get_subscriptions(context.channel.id)]
    if len(subscriptions) == 0:
        await context.send("No subscriptions.")
    else:
        message = "\n".join(subscriptions)
        await context.send(message)


@bot.command()
async def unsbscribe(context: commands.Context, url: str):
    if mongo.unsibscribe(context.channel.id, url):
        await context.send("Success")
    else:
        await context.send("Subscription not found.")


def run():
    bot.run(TOKEN)


if __name__ == "__main__":
    print("Start Discord RSS")
    print(f"[MongoDB Address] {mongo.MONGO_ADDRESS}")
    print(f"[Bot command prefix] {COMMAND_PREFIX}")
    print(f"[Bot crawl interval] {CRAWL_INTERVAL_MINUTES}(min)")
    run()