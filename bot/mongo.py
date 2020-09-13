import os
from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv(verbose=True)

# MongoDB Vairables
MONGO_USERNAME = os.environ.get("MONGO_USERNAME")
MONGO_PASSWORD = os.environ.get("MONGO_PASSWORD")
MONGO_ADDRESS = os.environ.get("MONGO_ADDRESS")
MONGO_CONNECTION_STRING = f"mongodb://{MONGO_USERNAME}:{MONGO_PASSWORD}@{MONGO_ADDRESS}"
MONGO_DB_NAME = "discord-rss"
MONGO_SUBSCRIPTIONS_COLLECTION = "subscriptions"
MONGO_POSTS_COLLECTION = "posts"
ID = "id"
CHANNEL_ID = "channel_id"
TITLE = "title"
URL = "url"


def connect():
    return MongoClient(MONGO_CONNECTION_STRING)


def get_subscriptions_collection(client: MongoClient):
    return client[MONGO_DB_NAME][MONGO_SUBSCRIPTIONS_COLLECTION]


def get_posts_collection(client: MongoClient):
    return client[MONGO_DB_NAME][MONGO_POSTS_COLLECTION]


def subscribe(channel_id: int, title: str, url: str):
    with connect() as client:
        subscriptions = get_subscriptions_collection(client)
        subscription = {
            CHANNEL_ID: channel_id,
            TITLE: title,
            URL: url
        }
        if subscriptions.find_one(subscription) is None:
            subscriptions.insert(subscription)


def unsibscribe(channel_id: int, url: str):
    with connect() as client:
        subscriptions = get_subscriptions_collection(client)
        filter = {
            CHANNEL_ID: channel_id,
            URL: url
        }
        if subscriptions.find_one_and_delete(filter) is None:
            return False
        return True


def get_subscriptions(channel_id: int=None):
    with connect() as client:
        filter = None if channel_id is None else { CHANNEL_ID: channel_id }
        return [
            {
                CHANNEL_ID: subscription[CHANNEL_ID],
                TITLE: subscription[TITLE],
                URL: subscription[URL]
            } 
            for subscription
            in get_subscriptions_collection(client).find(filter)
        ]

def get_all_subscription_urls(channel_id: int=None):
    return set([ subscription[URL] for subscription in get_subscriptions(channel_id) ])


def get_channel_ids(url: str=None):
    with connect() as client:
        filter = None if url is None else { URL: url }
        return set([
            subscription[CHANNEL_ID]
            for subscription 
            in get_subscriptions_collection(client).find(filter)
        ])


def feed(title: str, url: str) -> bool:
    with connect() as client:
        posts = get_posts_collection(client)
        post = {
            TITLE:title,
            URL: url
        }
        if posts.find_one(post):
            return False
        posts.insert(post)
        return True


def delete_channel_subscriptions(channel_id: int):
    with connect() as client:
        filter = {
            CHANNEL_ID: channel_id
        }
        get_subscriptions_collection(client).delete_many(filter)
