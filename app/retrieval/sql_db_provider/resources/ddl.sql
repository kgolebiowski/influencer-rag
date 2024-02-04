CREATE TABLE IF NOT EXISTS Channel (
    channelId INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    url TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS Movie (
     movieId INTEGER PRIMARY KEY AUTOINCREMENT,
     channelId INTEGER,
     title TEXT NOT NULL,
     url TEXT NOT NULL,
     keywords TEXT,
     summary TEXT,
     length INTEGER NOT NULL,
     FOREIGN KEY (channelId) REFERENCES channel (channelId) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS Paragraph (
     paragraphId INTEGER PRIMARY KEY AUTOINCREMENT,
     movieId INTEGER,
     content TEXT NOT NULL,
     FOREIGN KEY (movieId) REFERENCES movie (movieId) ON DELETE CASCADE
);
