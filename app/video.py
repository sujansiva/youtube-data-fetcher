from flask import (
    Blueprint, request
)

from app.db import get_db
from app.utils.api import fetch_video_data
from app.utils.db import (
    add_interactions_to_video_interactions_table,
    add_video_to_videos_table,
    get_pk_from_channels_table,
    get_pk_from_videos_table_by_video_id)

bp = Blueprint('video', __name__, url_prefix='/video')


@ bp.route('/fetch', methods=['POST'])
def fetch():
    args = request.args
    video_id = args.get('videoId')

    if video_id is None:
        return 'videoId is a required query parameter.', 400

    db = get_db()

    try:
        video_data = fetch_video_data(video_id)
        channel_id = get_pk_from_channels_table(
            db, video_data['youtube_channel_id'])
        add_video_to_videos_table(db, channel_id, video_id, video_data)

        video_pk = get_pk_from_videos_table_by_video_id(db, video_id)
        add_interactions_to_video_interactions_table(db, video_pk, video_data)

        db.commit()

        return 'Video data added to the database.'
    except:
        return 'Video data could not be added to the database.', 500
