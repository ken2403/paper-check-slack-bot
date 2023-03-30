# paper-check-slack-bot

![sample](https://github.com/ken2403/paper-check-slack-bot/blob/feat/images/image/sample.png)
An application that collects the latest articles from [arxiv](https://arxiv.org/), summarizes them with [chatGPT](https://openai.com/blog/chatgpt), and posts them to [slack](https://slack.com).

## Requirements

- [Python](https://www.python.org/) >= 3.7
- [arxiv](http://lukasschwab.me/arxiv.py/index.html) == 1.4.3
- [OpenAI Python Library](https://platform.openai.com/docs/api-reference?lang=python) == 0.27.2
- [python-dotenv](https://saurabh-kumar.com/python-dotenv/) == 1.0.0
- [Python Slack SDK](https://slack.dev/python-slack-sdk/) == 3.20.1

## Usage

1. Create the environment file.

   Copy `.env.sample` to `.env` and edit it.

    ```bash
    cp .env.sample .env
    ```

    Fill in the following environment variables.
    - `OPENAI_API_KEY`: OpenAI API key
    - `SLACK_API_TOKEN`: Slack bot API token

2. Create the argument file.

   Copy `args.json.sample` to `args/` directory and edit it.

    ```bash
    cp args.json.sample args/your_args.json
    ```

    Fill in the following arguments.
    - `news_title`: the title of the news
    - `post_channel`: the channel name to post the message
    - `categories`: array of arxiv categories
    - `max_results`: the maximum number of papers to post
    - `fetch_results`: the number of papers to fetch from arxiv

3. Build and run the docker container.  

    Build the docker container.

    ```bash
    cd paper-check-slack-bot
    (paper-check-slack-bot) docker-compose build
    ```

    Run the docker container with custom argument file.

    ```bash
    docker-compose run paper-check-slack-bot your_args.json
    ```

## Reference

- [article of Zenn](https://zenn.dev/ozushi/articles/ebe3f47bf50a86)
