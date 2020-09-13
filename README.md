# Discord RSS Bot

RSS bot for Discord.

## Hot to use.

1. Clone repository.

    ```sh
    git@github.com:reifujimura/discord-rss-bot.git
    ```

1. Rename .env.template to .env and edit.

    |Variable|Value|
    |:-|:-|
    |TOKEN|Your Discord bot auth token|
    |MONGO_USERNAME|MongoDB username|
    |MONGO_PASSWORD|MongoDB password|
    |Command prefix|Bot command prefix|
    |Crawl interval minutes|RSS crawl interval (min)|

1. Start service

    ```sh
    docker-compose up
    ```

## LISENCE

MIT License