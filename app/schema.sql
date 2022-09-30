DROP TABLE IF EXISTS channels;
DROP TABLE IF EXISTS videos;
DROP TABLE IF EXISTS video_interactions;

CREATE TABLE channels (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  channel_id VARCHAR(255) NOT NULL,
  url VARCHAR(255) NOT NULL,
  title TEXT NOT NULL,
  description TEXT NOT NULL,
  view_count INTEGER NOT NULL,
  subscriber_count INTEGER NOT NULL,
  video_count INTEGER NOT NULL,
  image_url VARCHAR(255),
  creation_date TIMESTAMP NOT NULL
);

CREATE TABLE videos (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  channel_id INTEGER NOT NULL,
  video_id VARCHAR(255) NOT NULL,
  url VARCHAR(255) NOT NULL,
  title TEXT NOT NULL,
  duration TEXT NOT NULL,
  image_url VARCHAR(255),
  published_date TIMESTAMP NOT NULL,
  FOREIGN KEY (channel_id) REFERENCES channels (id)
);

CREATE TABLE video_interactions (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  video_id INTEGER NOT NULL,
  view_count INTEGER NOT NULL,
  like_count INTEGER NOT NULL,
  comment_count INTEGER NOT NULL,
  latest BOOLEAN NOT NULL,
  FOREIGN KEY (video_id) REFERENCES videos (id)
);

CREATE INDEX idx_channels_channel_id ON channels (channel_id);

CREATE INDEX idx_videos_channel_id ON videos (channel_id);