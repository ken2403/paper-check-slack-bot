from __future__ import annotations

import os
import sys
import argparse
import pickle
import json
import datetime
import logging

import arxiv
from dotenv import load_dotenv
import openai
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")


def get_papers_from_arxiv(
    categories: list[str] = ["cs.LG", "physics.chem-ph"],
    max_results: int = 3,
    fetch_results: int = 20,
    delivered_ids: list[str] = [],
) -> tuple[list[arxiv.Result], list[str]]:
    # get papers
    query = " AND ".join([f"cat:{c}" for c in categories])
    search = arxiv.Search(
        query=query,
        max_results=fetch_results,
        sort_by=arxiv.SortCriterion.SubmittedDate,
        sort_order=arxiv.SortOrder.Descending,
    )
    results = list(search.results())

    # remove delivered papers
    response: list[arxiv.Result] = []
    num = 0
    for result in results:
        if result.entry_id not in delivered_ids:
            response.append(result)
            delivered_ids.append(result.entry_id)
            num += 1
        if num >= max_results:
            break

    return response, delivered_ids


def get_summary(result: arxiv.Result) -> str:
    system = """Please summarize the main points of the given paper in three points only and output them in Japanese
    in the following format.```
    - Main Point 1
    - Main Point 2
    - Main Point 3
    ```"""
    text = f"title: {result.title}\nbody: {result.summary}"
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": text},
        ],
        temperature=0.25,
    )

    summary = response["choices"][0]["message"]["content"]
    date_str = result.published.strftime("%Y-%m-%d %H:%M")
    message = f"""
    *Issue date*: {date_str}
    *ID*: {result.entry_id}
    *Title*: {result.title}
    *Summary*:
    {summary}
    """

    return message


def json2args(json_path: str) -> argparse.Namespace:
    with open(json_path) as f:
        args = argparse.Namespace(**json.load(f))
    return args


def main():
    file_name = sys.argv[1]
    args = json2args(f"/app/args/{file_name}")
    title = args.news_title
    today = datetime.datetime.now().strftime("%Y-%m-%d")

    # Get a delivered IDs
    ids_file = f"/app/args/{file_name.split('.')[0]}_id.p"
    if os.path.exists(ids_file):
        with open(ids_file, "rb") as f:
            delivered_ids: list[str] = pickle.load(f)
    else:
        delivered_ids: list[str] = []
    if len(delivered_ids) > args.fetch_results:
        delivered_ids = delivered_ids[: args.fetch_results]

    # Get papers
    papers, new_ids = get_papers_from_arxiv(
        args.categories, args.max_results, args.fetch_results, delivered_ids
    )

    # Push to slack
    client = WebClient(token=os.getenv("SLACK_API_TOKEN"))
    # no new message
    if len(papers) == 0:
        message = f"""
        :x: *{title}* ({today}) :x:
        *No new papers*
        """

        try:
            response = client.chat_postMessage(channel=args.post_channel, text=message)
            logger.info(f"Message posted: {response['ts']}")
        except SlackApiError as e:
            print(e)
            logger.info(f"Error posting: {e}")

        logger.info("No new papers")
        return
    # post new papers
    for i, result in enumerate(papers):
        # try:
        #     message = f"""
        #     :newspaper: *{title}* ({today}, {i+1}/{len(papers)}) :newspaper:
        #     {get_summary(result)}
        #     """
        # except Exception as e:
        #     logger.info(f"Error summarize {i}th paper: {e}")
        #     continue
        message = f"""
            :newspaper: *{title}* ({today}, {i+1}/{len(papers)}) :newspaper:
            *Issue date*: {result.published.strftime("%Y-%m-%d %H:%M")}
            *ID*: {result.entry_id}
            *Title*: {result.title}
            *Summary*:
            {result.summary}
            """

        try:
            response = client.chat_postMessage(channel=args.post_channel, text=message)
            logger.info(f"Message posted: {response['ts']}")
        except SlackApiError as e:
            print(e)
            logger.info(f"Error posting {i}th message: {e}")

    # Save delivered IDs
    with open(ids_file, "wb") as f:
        pickle.dump(new_ids, f)


if __name__ == "__main__":
    main()
