# Youtube Data Fetcher

This app contains a few routes to fetch and store data about YouTube channels and videos using the YouTube API.

It is built using Flask and SQLite.

To use this app, you need an API key for Youtube's Data API. Please set this API key as an environment variable with the name `YOUTUBE_API_KEY`.

Please install all of the app's dependencies using the following command:

```
pip install -r requirements.txt
```

This app offers the following commands for initializing an empty database, and seeding the database:

```
flask init-db
flask seed-db
```

To run the app locally, use the following command:

```
flask run
```

To add a new YouTube channel or video to the database, the following routes are available:

```
POST /channel/fetch?channelId=?
POST /video/fetch?videoId=?
```

To refresh the data for a channel and all of its associated videos in the database, the following route is available:

```
PUT /channel/refresh?channelId=?
```
