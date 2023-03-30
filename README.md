# paper-check-slack-bot

## Requirements

- [Python](https://www.python.org/) >= 3.7
- [arxiv](http://lukasschwab.me/arxiv.py/index.html) == 1.4.3
- [OpenAI Python Library](https://platform.openai.com/docs/api-reference?lang=python) == 0.27.2
- [python-dotenv](https://saurabh-kumar.com/python-dotenv/) == 1.0.0
- [Python Slack SDK](https://slack.dev/python-slack-sdk/) == 3.20.1

## Usage

1. Create the argument file.
    copy `args.json.sample` to `args/` directory and edit it.

    ```bash
    cp args.json.sample args/your_name.json
    ```

2. Build and run the docker container.

    ```bash
    cd paper-check-slack-bot
    (paper-check-slack-bot) docker-compose build
    ```

    Run the docker container.

    ```bash
    docker-compose run slack-bot
    ```

## Reference

- [article of Zenn](https://zenn.dev/ozushi/articles/ebe3f47bf50a86)
