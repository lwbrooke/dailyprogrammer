#!/usr/bin/env python3

from datetime import datetime
from dateutil import parser
import click
import os
import os.path
import praw
import pytz
import re
import shutil
import sys

_SITE_NAME = 'dailyprogrammer-bot'
_SUBREDDIT = 'dailyprogrammer'
_DATE_FORMAT = '%Y-%m-%d'
_RATING_PATTERN = r'(?<=\[)(?!psa)[a-z]*(?=\])'
_SANITIZE_PATTERN = r'(\[[0-9-/]+\]|\[[a-z/]+\]|[^0-9a-z\s])'
_SYMBOL_PATTERN = r'[^0-9a-z\s]'
_WEEKLY_MONTHLY_PATTERN = r'(monthly|weekly|week-long)'
_KNOWN_DIRECTORIES = (
    'all',
    'bonus',
    'difficult',
    'easy',
    'extra',
    'hard',
    'intermediate',
    'medium',
    'monthly',
    'special',
    'unknown',
    'weekly'
)
_TITLE_IDENTIFIERS = (
    'challenge #',
    'chalenge #',
    'weekly #'
)


@click.group()
def cli():
    """A cli for pulling and managing challenges from r/dailyprogrammer."""
    pass


@cli.command()
@click.argument('start')
@click.argument('end', required=False, default='')
@click.option('-t', '--timezone', metavar='TZ', default='America/Los_Angeles', show_default=True,
              help='Specify a timezone for the date range')
def pull(start, end, timezone):
    """
    Pull challenges for the specified START and END times.

    START and END must be parsable by dateutil.parser.parse with the following exception.
    START can be either 'all' or 'today', which will automatically pick your START and
    END times. In this case END will be ignored if provided.
    """
    if start == 'all':
        kwargs = {}
    elif start == 'today':
        try:
            timezone = pytz.timezone(timezone)
        except pytz.UnknownTimeZoneError:
            click.echo('"{}" is an unknown timezone'.format(timezone))
            sys.exit(1)

        now = datetime.now(timezone)
        start = datetime(now.year, now.month, now.day, 0, 0, 0, tzinfo=timezone).timestamp()
        end = datetime(now.year, now.month, now.day, 23, 59, 59, tzinfo=timezone).timestamp()
        kwargs = {'start': start, 'end': end}
    else:
        try:
            start = parser.parse(start).timestamp()
        except ValueError:
            click.echo('"{}" is unparsable as a datetime'.format(start))
            sys.exit(1)
        try:
            end = parser.parse(end).timestamp()
        except ValueError:
            click.echo('"{}" is unparsable as a datetime'.format(end))
            sys.exit(1)
        if start > end:
            click.echo('start must be before end')
            sys.exit(1)

        kwargs = {'start': start, 'end': end}

    _get_challenges(**kwargs)


@cli.command()
def clean():
    """
    Destroy the directories that challenges are located in to prepare for a clean pull.

    \b
    Known directories:
    ./all
    ./bonus
    ./difficult
    ./easy
    ./extra
    ./hard
    ./intermediate
    ./medium
    ./monthly
    ./special
    ./unknown
    ./weekly
    """
    for d in _KNOWN_DIRECTORIES:
        try:
            shutil.rmtree(d)
        except FileNotFoundError:
            continue


def _get_challenges(start=None, end=None):
    reddit = praw.Reddit(_SITE_NAME)
    subreddit = reddit.subreddit(_SUBREDDIT)
    for submission in subreddit.submissions(start=start, end=end):
        _parse(submission)


def _parse(submission):
    title = submission.title.lower()
    if all(i not in title for i in _TITLE_IDENTIFIERS):
        return

    sub_date = datetime.fromtimestamp(submission.created_utc).strftime(_DATE_FORMAT)
    rating = _get_challenge_rating(title)
    sanitized_title = _sanitize_title(title)

    challenge_dir = os.path.join(os.getcwd(), '{}/{}_{}/'.format(rating, sub_date, sanitized_title))
    click.echo(challenge_dir)
    os.makedirs(challenge_dir, exist_ok=True)

    readme = '# {}\n\n{}\n\n{}\n'.format(submission.title, submission.selftext, submission.url)
    with open(os.path.join(challenge_dir, 'README.md'), 'w') as f_out:
        f_out.write(readme)


def _get_challenge_rating(title):
    match = re.search(_RATING_PATTERN, title) or re.search(_WEEKLY_MONTHLY_PATTERN, title)
    return re.sub(_SYMBOL_PATTERN, '-', match.group() if match else 'unknown')


def _sanitize_title(title):
    return '-'.join(re.sub(_SANITIZE_PATTERN, ' ', title).split())


if __name__ == '__main__':
    cli()
