from flask import (
    Blueprint, request
)

from app.db import get_db
from app.utils.api import fetch_channel_data, fetch_video_data
from app.utils.db import (
    add_channel_to_channels_table,
    batch_add_interactions_to_video_interactions_table,
    get_pk_from_channels_table,
    get_video_from_videos_table_by_channel_id,
    update_channel_in_channels_table,
    update_most_recent_interactions_in_video_interactions_table)

bp = Blueprint('channel', __name__, url_prefix='/channel')


@bp.route('/fetch', methods=['POST'])
def fetch():
    args = request.args
    channel_id = args.get('channelId')

    if channel_id is None:
        return 'channelId is a required query parameter.', 400

    db = get_db()

    try:
        channel_data = fetch_channel_data(channel_id)
        add_channel_to_channels_table(db, channel_id, channel_data)

        db.commit()
        return 'Channel data added to the database.'
    except:
        return 'Channel data could not be added to the database.', 500


@bp.route('/refresh', methods=['PUT'])
def refresh():
    args = request.args
    channel_id = args.get('channelId')

    if channel_id is None:
        return 'channelId is a required query parameter.', 400

    db = get_db()

    channel_pk = get_pk_from_channels_table(db, channel_id)

    if channel_pk == 0:
        return f'A channel could not be found in the database with channel_id: {channel_id}', 400

    try:
        channel_data = fetch_channel_data(channel_id)
        update_channel_in_channels_table(db, channel_pk, channel_data)
    except:
        db.rollback()
        return 'Channel data could not be refreshed in the database.', 500

    associated_videos = get_video_from_videos_table_by_channel_id(
        db, channel_pk)

    existing_video_interactions_to_update = []
    new_video_interactions_to_insert = []

    for video in associated_videos:
        video_pk = video['id']
        video_id = video['video_id']

        existing_video_interactions_to_update.append((video_pk,))

        video_data = fetch_video_data(video_id)
        new_video_interactions_to_insert.append(
            (video_pk, video_data['view_count'], video_data['like_count'], video_data['comment_count'], 1,))

    try:
        # update the existing row by setting latest to 0, then insert a new row with fresh data
        update_most_recent_interactions_in_video_interactions_table(
            db, existing_video_interactions_to_update)
        batch_add_interactions_to_video_interactions_table(
            db, new_video_interactions_to_insert)
    except:
        db.rollback()
        return 'Channel data could not be refreshed in the database.', 500

    db.commit()
    return f'The data has been refreshed for channel {channel_id} and all of its associated videos'
