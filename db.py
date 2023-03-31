"""
MySQL database, that keeps data about lessons
"""

import mysql.connector
import question


class DataBase:
    """
    'Mnogomov' database for keeping data for questions and lessons, such as:
    question texts, answer options, correct answers, words definitions, etc.
    """

    def __init__(self):
        self.db = mysql.connector.connect(
            host="localhost",
            user="root",
            password="root",
            port='3306',
            database="mnogomov"
        )

    def get_questions_data(self) -> list:
        """
        Get questions from db using MySQL

        :return: list with questions
        """
        cursor = self.db.cursor()
        query = "SELECT * FROM lesson"
        cursor.execute(query)
        questions = cursor.fetchall()
        cursor.close()
        return [question.Question(*q) for q in questions]

    def close_db(self) -> None:
        """
        Close connection with db

        :return: None
        """
        self.db.close()
