import sqlite3
import click
import os
import requests
import math
from flask import current_app, g


def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db


def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()


def init_db():
    db = get_db()

    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))


def seed_db():
    db = get_db()

    seed_data_channel_ids = ['UC9CoOnJkIBMdeijd9qYoT_g', 'UCiGm_E4ZwYSHV3bcW1pnSeQ',
                             'UCAvCL8hyXjSUHKEGuUPr1BA', 'UCIwFjwMjI0y7PDBVEO9-bkQ']
    seed_data_video_ids = ['tcYodQoapMg', 'r2XJ9P1NvJc', '5GJWxDKyk3A',
                           'V1Pl8CzNzCw', 'Pkh8UtuejGw', 'KkGVmN68ByU', 'tQ0yjYUFKAE', 'xFJjczkU4So']

    key = os.environ.get('YOUTUBE_API_KEY')
    db = get_db()

    for channel_id in seed_data_channel_ids:
        try:
            r = requests.get(
                f'https://youtube.googleapis.com/youtube/v3/channels?part=snippet%2Cstatistics&id={channel_id}&key={key}')
            body = r.json()['items'][0]

            url = f'https://www.youtube.com/channel/{channel_id}'
            title = body['snippet']['title']
            description = body['snippet']['description']
            view_count = body['statistics']['viewCount']
            subscriber_count = body['statistics']['subscriberCount']
            video_count = body['statistics']['videoCount']
            image_url = body['snippet']['thumbnails']['default']['url']
            creation_date = body['snippet']['publishedAt']

            db.execute(
                "INSERT INTO channels (channel_id, url, title, description, view_count, subscriber_count, video_count, image_url, creation_date) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                (channel_id, url, title, description, view_count,
                 subscriber_count, video_count, image_url, creation_date),
            )
            db.commit()
        except:
            return f'Could not insert data for {channel_id} into the database.'

    cid = 1.0
    for video_id in seed_data_video_ids:
        try:
            r = requests.get(
                f'https://youtube.googleapis.com/youtube/v3/videos?part=snippet%2Cid%2CcontentDetails%2Cstatistics&id={video_id}&key={key}')
            body = r.json()['items'][0]

            channel_id = int(math.floor(cid))
            url = f'https://www.youtube.com/watch?v={video_id}'
            title = body['snippet']['title']
            view_count = body['statistics']['viewCount']
            like_count = body['statistics']['likeCount']
            comment_count = body['statistics']['commentCount']
            duration = body['contentDetails']['duration']
            image_url = body['snippet']['thumbnails']['default']['url']
            published_date = body['snippet']['publishedAt']

            db.execute(
                "INSERT INTO videos (channel_id, video_id, url, title, duration, image_url, published_date) VALUES (?, ?, ?, ?, ?, ?, ?)",
                (channel_id, video_id, url, title,
                 duration, image_url, published_date),
            )

            video_result = db.execute(
                'SELECT id FROM videos where video_id = ?', (video_id,)).fetchone()
            video_pk = video_result[0]

            db.execute(
                "INSERT INTO video_interactions (video_id, view_count, like_count, comment_count, latest) VALUES (?, ?, ?, ?, ?)",
                (video_pk, view_count, like_count, comment_count, 1),
            )

            db.commit()
        except:
            return f'Could not insert data for {video_id} into the database.'

        cid += 0.5


@click.command('init-db')
def init_db_command():
    """Clear the existing data and create new empty tables."""
    init_db()
    click.echo('Initialized the database.')


@click.command('seed-db')
def seed_db_command():
    """Clear the existing data and create new populated tables."""
    init_db()
    seed_db()
    click.echo('Initialized and seeded the database.')


def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
    app.cli.add_command(seed_db_command)
