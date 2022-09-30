import sqlite3
import click
import math
from flask import current_app, g

from .utils.api import fetch_channel_data, fetch_video_data
from .utils.db import (
    add_channel_to_channels_table,
    add_interactions_to_video_interactions_table,
    add_video_to_videos_table,
    get_pk_from_videos_table_by_video_id)


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

    db = get_db()

    for channel_id in seed_data_channel_ids:
        try:
            channel_data = fetch_channel_data(channel_id)
            add_channel_to_channels_table(db, channel_id, channel_data)

            db.commit()
        except:
            return f'Could not insert data for {channel_id} into the database.'

    cid = 1.0
    for video_id in seed_data_video_ids:
        try:
            video_data = fetch_video_data(video_id)
            channel_id = int(math.floor(cid))

            add_video_to_videos_table(db, channel_id, video_id, video_data)
            video_pk = get_pk_from_videos_table_by_video_id(db, video_id)
            add_interactions_to_video_interactions_table(
                db, video_pk, video_data)

            db.commit()
        except:
            return f'Could not insert data for {video_id} into the database.'

        cid += 0.5


@ click.command('init-db')
def init_db_command():
    """Clear the existing data and create new empty tables."""
    init_db()
    click.echo('Initialized the database.')


@ click.command('seed-db')
def seed_db_command():
    """Clear the existing data and create new populated tables."""
    init_db()
    seed_db()
    click.echo('Initialized and seeded the database.')


def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
    app.cli.add_command(seed_db_command)
