import os
import unittest

from app.retrieval.sql_db_provider.sql_db_provider_sqlite import SQLiteProvider


class SQLiteProviderTest(unittest.TestCase):

    test_db_path: str = "tests/test_data/app_database.db"
    sqlite_provider: SQLiteProvider

    @classmethod
    def setUpClass(cls):
        os.makedirs(os.path.dirname(cls.test_db_path), exist_ok=True)
        cls.sqlite_provider: SQLiteProvider = SQLiteProvider(cls.test_db_path)

    def test_should_create_schema(self):
        results = self.sqlite_provider.run_query(
            "SELECT name FROM sqlite_master "
            "WHERE type = 'table' and name in ('Channel', 'Movie', 'Paragraph')")

        self.assertEqual(len(results), 3)

    def test_should_create_and_delete_sample_data(self):
        sample_channel = {
            'title': 'Greg Kamradt (Data Indy)',
            'url': 'https://www.youtube.com/@DataIndependent'
        }

        channel_id1 = self.sqlite_provider.add_channel(
            sample_channel['title'], sample_channel['url'])

        self.sqlite_provider.cursor.execute("SELECT * FROM channel WHERE channelId=?", (channel_id1,))
        channel1 = self.sqlite_provider.cursor.fetchone()
        self.assertIsNotNone(channel1)
        self.assertEqual(channel1[1], sample_channel['title'])

        sample_movie = {
            'channel_id': channel_id1,
            'title': 'Is ESG Investing Counterproductive?',
            'url': 'https://www.youtube.com/watch?v=c4AMFicXXqg',
            'keywords': 'openai, chatgpt',
            'summary':
                "Breaking news, New York City bans artificial intelligence from its public networks to keep "
                "students and teachers safe. doesn't that sound like a headline from a movie about an AI apocalypse. "
                "But no, it's real. It's here now. And we are going to hear more headlines like this in 2023 "
                "Take a listen.",
            'length': 120,
            'paragraphs': [
                "Breaking news, New York City bans artificial intelligence from its public networks to keep "
                "students and teachers safe. doesn't that sound like a headline from a movie about an AI apocalypse. "
                "But no, it's real. It's here now. And we are going to hear more headlines like this in 2023 "
                "Take a listen.",

                "Your tech is called chat GPT that allows users to ask it questions. "
                "The bot then spits out realistic human-like responses. The New York City Department of Education "
                "has restricted the tool on all city public school networks and devices. OpenAI released chat GPT "
                "in November 2022 and it has a lot of people concerned about safety news anchors and politicians "
                "are fear-mongering about the face melting rise of artificially intelligent systems, "
                "Creative people and software engineers are concerned about this AI taking their jobs. "
                "And now a few months after Chad GPT is released, the first shots are fired as New York City bands "
                "chat GPt on all of its school networks due to concerns about negative impact on student learning. "
                "and concern regarding the safety and accuracy of content access to chat.",

                " GPT is restricted on New York City Public schools networks and devices education "
                "Department spokesperson Jenna Lyle said, while the two might be able to provide quick and "
                "easy access and answers to questions, it does not build critical thinking and problem-solving skills, "
                "which are essential for academic and lifelong success, meaning that kids are using it to "
                "cheat on their homework. Teachers are in panic mode over this tool. When shown, "
                "Chad GPT writing side by side with student writing, teachers, and educators cannot "
                "tell them apart when students were asked about Chad GBT, and if they used it for school, "
                "some of them were genuinely surprised that the teachers even knew what Chad GPT was, "
                "which is kind of funny. If you want to know the latest on the AI revolution that we are "
                "living through right now, click subscribe, and thank you for watching."
            ]
        }

        movie_id = self.sqlite_provider.add_movie(
            sample_movie['channel_id'], sample_movie['title'], sample_movie['url'], sample_movie['keywords'],
            sample_movie['summary'], sample_movie['length'], sample_movie['paragraphs'])

        self.sqlite_provider.cursor.execute("SELECT * FROM movie WHERE movieId=?", (movie_id,))
        movie = self.sqlite_provider.cursor.fetchone()
        self.assertIsNotNone(movie)
        self.assertEqual(movie[2], sample_movie['title'])

        self.sqlite_provider.cursor.execute("SELECT * FROM paragraph WHERE movieId=?", (movie_id,))
        paragraphs = self.sqlite_provider.cursor.fetchall()
        self.assertEqual(len(paragraphs), 3)
        self.assertEqual(paragraphs[0][2], sample_movie['paragraphs'][0])
        self.assertEqual(paragraphs[1][2], sample_movie['paragraphs'][1])
        self.assertEqual(paragraphs[2][2], sample_movie['paragraphs'][2])

        self.sqlite_provider.clear_all_data()

        self.sqlite_provider.cursor.execute("SELECT count(*) FROM channel")
        row_count = self.sqlite_provider.cursor.fetchone()
        self.assertIsNotNone(row_count)
        self.assertEqual(row_count[0], 0)

        self.sqlite_provider.cursor.execute("SELECT count(*) FROM movie")
        row_count = self.sqlite_provider.cursor.fetchone()
        self.assertIsNotNone(row_count)
        self.assertEqual(row_count[0], 0)

        self.sqlite_provider.cursor.execute("SELECT count(*) FROM paragraph")
        row_count = self.sqlite_provider.cursor.fetchone()
        self.assertIsNotNone(row_count)
        self.assertEqual(row_count[0], 0)

    @classmethod
    def tearDownClass(cls):
        cls.sqlite_provider.close()
        os.remove(cls.test_db_path)


if __name__ == '__main__':
    unittest.main()
