def add_channel_to_channels_table(db, channel_id, channel_data):
    db.execute(
        "INSERT INTO channels (channel_id, url, title, description, view_count, subscriber_count, video_count, image_url, creation_date) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
        (channel_id, channel_data['url'], channel_data['title'], channel_data['description'], channel_data['view_count'],
         channel_data['subscriber_count'], channel_data['video_count'], channel_data['image_url'], channel_data['creation_date']),
    )


def update_channel_in_channels_table(db, channel_pk, channel_data):
    db.execute(
        'UPDATE channels SET title = ?, description = ?, view_count = ?, subscriber_count = ?, video_count = ?, image_url = ?'
        ' WHERE id = ?',
        (channel_data['title'], channel_data['description'], channel_data['view_count'],
         channel_data['subscriber_count'], channel_data['video_count'], channel_data['image_url'], channel_pk)
    )


def add_video_to_videos_table(db, channel_id, video_id, video_data):
    db.execute(
        "INSERT INTO videos (channel_id, video_id, url, title, duration, image_url, published_date) VALUES (?, ?, ?, ?, ?, ?, ?)",
        (channel_id, video_id, video_data['url'], video_data['title'],
         video_data['duration'], video_data['image_url'], video_data['published_date']),
    )


def add_interactions_to_video_interactions_table(db, video_id, video_data):
    db.execute(
        "INSERT INTO video_interactions (video_id, view_count, like_count, comment_count, latest) VALUES (?, ?, ?, ?, ?)",
        (video_id, video_data['view_count'],
         video_data['like_count'], video_data['comment_count'], 1),
    )


def update_most_recent_interaction_in_video_interactions_table(db, video_pk):
    db.execute(
        'UPDATE video_interactions SET latest = 0 WHERE video_id = ? AND latest = 1', (video_pk,))


def get_pk_from_videos_table_by_video_id(db, video_id):
    video_result = db.execute(
        'SELECT id FROM videos where video_id = ?', (video_id,)).fetchone()
    return video_result[0]


def get_pks_from_videos_table_by_channel_id(db, channel_id):
    video_results = db.execute(
        'SELECT id, video_id FROM videos WHERE channel_id = ?', (channel_id,)).fetchall()
    return video_results


def get_pk_from_channels_table(db, channel_id):
    channel_result = db.execute(
        'SELECT id FROM channels WHERE channel_id = ?', (channel_id,)).fetchone()

    return channel_result[0] if channel_result else 0
