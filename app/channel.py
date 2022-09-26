import requests
import os

from flask import (
    Blueprint, request
)

from app.db import get_db

bp = Blueprint('channel', __name__, url_prefix='/channel')


@bp.route('/fetch', methods=['POST'])
def fetch():
    args = request.args
    channel_id = args.get('channelId')

    if channel_id is None:
        return 'channelId is a required query parameter.', 400

    key = os.environ.get('YOUTUBE_API_KEY')
    db = get_db()

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

        return f'Channel data added to the database for {title}.'
    except:
        return 'Channel data could not be added to the database.', 500


@bp.route('/refresh', methods=['PUT'])
def refresh():
    args = request.args
    channel_id = args.get('channelId')

    if channel_id is None:
        return 'channelId is a required query parameter.', 400

    key = os.environ.get('YOUTUBE_API_KEY')
    db = get_db()

    channel_result = db.execute(
        'SELECT id FROM channels where channel_id = ?', (channel_id,)).fetchone()

    if channel_result is None:
        return f'A channel could not be found in the database with channel_id: {channel_id}', 400

    channel_pk = channel_result[0]

    try:
        r = requests.get(
            f'https://youtube.googleapis.com/youtube/v3/channels?part=snippet%2Cstatistics&id={channel_id}&key={key}')
        body = r.json()['items'][0]

        title = body['snippet']['title']
        description = body['snippet']['description']
        view_count = body['statistics']['viewCount']
        subscriber_count = body['statistics']['subscriberCount']
        video_count = body['statistics']['videoCount']
        image_url = body['snippet']['thumbnails']['default']['url']

        db.execute(
            'UPDATE channels SET title = ?, description = ?, view_count = ?, subscriber_count = ?, video_count = ?, image_url = ?'
            ' WHERE id = ?',
            (title, description, view_count,
             subscriber_count, video_count, image_url, channel_pk)
        )
    except:
        return 'Channel data could not be refreshed in the database.', 500

    video_results = db.execute(
        'SELECT id, video_id FROM videos WHERE channel_id = ? AND latest = ?', (channel_pk, 1,)).fetchall()

    for video in video_results:
        id = video['id']
        video_id = video['video_id']

        try:
            r = requests.get(
                f'https://youtube.googleapis.com/youtube/v3/videos?part=snippet%2Cid%2CcontentDetails%2Cstatistics&id={video_id}&key={key}')
            body = r.json()['items'][0]

            url = f'https://www.youtube.com/watch?v={video_id}'
            title = body['snippet']['title']
            view_count = body['statistics']['viewCount']
            like_count = body['statistics']['likeCount']
            comment_count = body['statistics']['commentCount']
            duration = body['contentDetails']['duration']
            image_url = body['snippet']['thumbnails']['default']['url']
            published_date = body['snippet']['publishedAt']

            # update the existing row by setting latest to 0, then insert a new row with fresh data
            db.execute('UPDATE videos SET latest = 0 WHERE id = ?', (id,))
            db.execute(
                "INSERT INTO videos (channel_id, video_id, url, title, view_count, like_count, comment_count, duration, image_url, published_date, latest) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                (channel_pk, video_id, url, title, view_count, like_count,
                 comment_count, duration, image_url, published_date, 1),
            )
        except:
            return 'Channel data could not be refreshed in the database.', 500

    db.commit()
    return f'The data has been refreshed for channel {channel_id} and all of its associated videos'
