import os
import requests

key = os.environ.get('YOUTUBE_API_KEY')


def fetch_channel_data(channel_id):
    r = requests.get(
        f'https://youtube.googleapis.com/youtube/v3/channels?part=snippet%2Cstatistics&id={channel_id}&key={key}')
    body = r.json()['items'][0]

    return {
        'url': f'https://www.youtube.com/channel/{channel_id}',
        'title': body['snippet']['title'],
        'description': body['snippet']['description'],
        'view_count': body['statistics']['viewCount'],
        'subscriber_count': body['statistics']['subscriberCount'],
        'video_count': body['statistics']['videoCount'],
        'image_url': body['snippet']['thumbnails']['default']['url'],
        'creation_date': body['snippet']['publishedAt']
    }


def fetch_video_data(video_id):
    r = requests.get(
        f'https://youtube.googleapis.com/youtube/v3/videos?part=snippet%2Cid%2CcontentDetails%2Cstatistics&id={video_id}&key={key}')
    body = r.json()['items'][0]

    return {
        'youtube_channel_id': body['snippet']['channelId'],
        'url': f'https://www.youtube.com/watch?v={video_id}',
        'title': body['snippet']['title'],
        'view_count': body['statistics']['viewCount'],
        'like_count': body['statistics']['likeCount'],
        'comment_count': body['statistics']['commentCount'],
        'duration': body['contentDetails']['duration'],
        'image_url': body['snippet']['thumbnails']['default']['url'],
        'published_date': body['snippet']['publishedAt']
    }
