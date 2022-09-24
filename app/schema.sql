DROP TABLE IF EXISTS channel;
DROP TABLE IF EXISTS video;

CREATE TABLE channel (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  url VARCHAR(255) NOT NULL,
  title TEXT NOT NULL,
  description TEXT NOT NULL,
  view_count INTEGER NOT NULL,
  subscriber_count INTEGER NOT NULL,
  video_count INTEGER NOT NULL,
  image_url VARCHAR(255),
  creation_date TIMESTAMP NOT NULL
);

CREATE TABLE video (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  channel_id INTEGER NOT NULL,
  url VARCHAR(255) NOT NULL,
  title TEXT NOT NULL,
  view_count INTEGER NOT NULL,
  like_count INTEGER NOT NULL,
  comment_count INTEGER NOT NULL,
  duration TEXT NOT NULL,
  image_url VARCHAR(255),
  published_date TIMESTAMP NOT NULL,
  FOREIGN KEY (channel_id) REFERENCES channel (id)
);