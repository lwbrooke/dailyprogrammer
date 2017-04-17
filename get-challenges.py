#!/usr/bin/env python3

from datetime import datetime, timezone
import click
import os.path
import os
import praw
import pytz
import re

_SITE_NAME = 'dailyprogrammer-bot'
_SUBREDDIT = 'dailyprogrammer'
_FIRST_SUBMISSION_DATE = datetime(2012, 2, 9, tzinfo=pytz.timezone('America/Los_Angeles'))
_DATE_FORMAT = '%Y-%m-%d'
_RATING_PATTERN = r'(?<=\[)(?!psa)[a-z]*(?=\])'
_SANITIZE_PATTERN = r'(\[[0-9/]+\]|\[[a-z/]+\]|[^0-9a-z\s])'
_SYMBOL_PATTERN = r'[^0-9a-z\s]'
_WEEKLY_MONTHLY_PATTERN = r'(monthly|weekly)'


@click.group()
def cli():
    pass


@cli.command('all')
def get_all():
    reddit = praw.Reddit(_SITE_NAME)
    subreddit = reddit.subreddit(_SUBREDDIT)
    for submission in subreddit.submissions():
        _parse(submission)


@cli.command('today')
def get_today():
    reddit = praw.Reddit(_SITE_NAME)
    subreddit = reddit.subreddit(_SUBREDDIT)
    today = datetime.utcnow()
    start, end = _get_day_boundaries(today.year, today.month, today.day)
    for submission in subreddit.submissions(start=start, end=end):
        _parse(submission)


def _parse(submission):
    os.getcwd()
    title = submission.title.lower()
    if 'challenge #' not in title and 'weekly #' not in title:
        return
    sub_date = datetime.fromtimestamp(submission.created_utc).strftime(_DATE_FORMAT)
    rating = _get_challenge_rating(title)
    sanitized_title = _sanitize_title(title)
    challenge_dir = os.path.join(os.getcwd(), '{}/{}_{}/'.format(rating, sub_date, sanitized_title))
    os.makedirs(challenge_dir, exist_ok=True)
    click.echo(challenge_dir)
    readme = '{}\n\n{}\n\n{}\n'.format(submission.title, submission.selftext, submission.url)
    with open(os.path.join(challenge_dir, 'README.md'), 'w') as f_out:
        f_out.write(readme)


def _get_challenge_rating(title):
    match = re.search(_RATING_PATTERN, title) or re.search(_WEEKLY_MONTHLY_PATTERN, title)
    return re.sub(_SYMBOL_PATTERN, '-', match.group() if match else 'unknown')


def _sanitize_title(title):
    return '-'.join(re.sub(_SANITIZE_PATTERN, ' ', title).split())


def _get_day_boundaries(year, month, day):
    start = datetime(year, month, day, 0, 0, 0, tzinfo=timezone.utc)
    end = datetime(year, month, day, 23, 59, 59, tzinfo=timezone.utc)
    return start.timestamp(), end.timestamp()


if __name__ == '__main__':
    cli()
