import requests
import os

from flask import (
    Blueprint, request
)

from app.db import get_db

bp = Blueprint('video', __name__, url_prefix='/video')


@bp.route('/fetch', methods=['POST'])
def fetch():
    args = request.args
    video_id = args.get('videoId')

    if video_id is None:
        return 'videoId is a required query parameter.', 400

    key = os.environ.get('YOUTUBE_API_KEY')
    db = get_db()

    try:
        r = requests.get(
            f'https://youtube.googleapis.com/youtube/v3/videos?part=snippet%2Cid%2CcontentDetails%2Cstatistics&id={video_id}&key={key}')
        body = r.json()['items'][0]

        channel_id = 1
        url = f'https://www.youtube.com/watch?v={video_id}'
        title = body['snippet']['title']
        view_count = body['statistics']['viewCount']
        like_count = body['statistics']['likeCount']
        comment_count = body['statistics']['commentCount']
        duration = body['contentDetails']['duration']
        image_url = body['snippet']['thumbnails']['default']['url']
        published_date = body['snippet']['publishedAt']

        db.execute(
            "INSERT INTO videos (channel_id, video_id, url, title, view_count, like_count, comment_count, duration, image_url, published_date, latest) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (channel_id, video_id, url, title, view_count, like_count,
             comment_count, duration, image_url, published_date, 1),
        )
        db.commit()

        return f'Video data added to the database for {title}.'
    except:
        return 'Video data could not be added to the database.', 500
