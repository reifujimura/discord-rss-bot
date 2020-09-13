import feedparser


def get_title(url: str):
    result = feedparser.parse(url)
    if result.bozo == 0 and result.version is not None:
        return result.feed.title
    return None


def get_feeds(url: str) -> list:
    feeds = []
    result = feedparser.parse(url)
    if result.status == 200:
        for entry in result.entries:
            feeds.append((entry.title, entry.link))
    return feeds
