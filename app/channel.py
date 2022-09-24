import requests

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
        r = requests.get(f'https://youtube.googleapis.com/youtube/v3/channels?part=snippet%2Cstatistics&id={channel_id}&key={key}')
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
            "INSERT INTO channel (url, title, description, view_count, subscriber_count, video_count, image_url, creation_date) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
            (url, title, description, view_count, subscriber_count, video_count, image_url, creation_date),
        )
        db.commit()

        return f'Channel data added to the database for {title}.'
    except:
        return 'Channel data could not be added to the database.', 500