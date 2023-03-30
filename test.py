"""
OOP-ed 'Mnogomov' after Eugene fucked up drastically
"""

from flask import Flask, render_template, request, redirect, url_for
import mysql.connector

app = Flask(__name__, template_folder="../Mnogomov/templates")
app.secret_key = "BE_Cheporte_157E3_Legion"


class Question:
    """
    Take retrieved data from 'mnogomov' db and use it to form a question, which
    will be displayed during a lesson.
    """

    def __init__(self,
                 id_question: int,
                 question_text: str,
                 option1: str,
                 option2: str,
                 option3: str,
                 answer: str,
                 content: str):
        self.id = id_question
        self.text = question_text
        self.options = [option1, option2, option3]
        self.answer = answer
        self.content = content

    def correct(self, user_answer: str) -> bool:
        """
        Check if user has answered correctly

        :param user_answer: user choice, one of three possible options (1, 2 or 3)
        :return: True if correct, else False
        """
        return str(self.answer) == user_answer

    def to_dict(self) -> dict:
        """
        Convert question data into dictionary for keeping data if needed.

        :return: dictionary with question parameters
        """
        return {
            "id": self.id,
            "question text": self.text,
            "options": self.options,
            "correct answer": self.answer
        }


class LessonQuiz:
    """
    Generate several question into one solis quiz which will be used for
    handling language lessons.
    """

    def __init__(self, questions):
        self.questions = questions
        self.current_q_idx = 0
        self.score = 0

    def get_score(self) -> int:
        """
        Return user score after lesson

        :return: integer representing user score
        """
        return self.score

    def reset_lesson(self) -> None:
        """
        Reset score and question index

        :return: None
        """
        self.score = 0
        self.current_q_idx = 0

    def current_q(self) -> Question:
        """
        Return data of question with specific index to be displayed
        """
        return self.questions[self.current_q_idx]

    def check_answers(self, user_answer):
        """
        Check user answers and change score according to results
        """
        if self.current_q().correct(user_answer):
            self.score += 1
        self.current_q_idx += 1

    def is_finished(self) -> bool:
        """
        Check if user has answered all questions

        :return: True if all questions are answered, else False
        """
        return self.current_q_idx >= len(self.questions) or self.current_q_idx >= 10

    def to_dict(self) -> dict:
        """
        Convert questions data into dictionary for keeping data if needed.

        :return: dictionary with questions
        """
        return {
            "questions": [q.to_dict() for q in self.questions],
            "current_q_idx": self.current_q_idx,
            "score": self.score
        }


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
        return [Question(*q) for q in questions]

    def close_db(self) -> None:
        """
        Close connection with db

        :return: None
        """
        self.db.close()


class App:
    """
    WebApp itself
    """

    def __init__(self):
        self.db = DataBase()
        self.lesson = LessonQuiz(self.db.get_questions_data())

    @staticmethod
    @app.route('/')
    def main():
        return render_template('main.html')

    @staticmethod
    @app.route('/homepage')
    def show_homepage():
        """
        Render home.html to display a homepage.
        """
        # ? =====================================================
        # ? if mnogomov_webapp.lesson.is_finished():
        # ?    return redirect(url_for('show_score'))
        # ? =====================================================
        mnogomov_webapp.lesson.current_q_idx = 0
        return render_template('home.html')

    @staticmethod
    @app.route('/about')
    def show_about():
        """
        Render about.html to display about page.
        """
        return render_template('about.html')

    @staticmethod
    @app.route('/vocabulary')
    def show_vocabulary():
        """
        Render vocabulary.html to display vocabulary for each lesson.
        """
        return render_template('vocabulary.html')

    @staticmethod
    @app.route('/lesson')
    def display_question():
        """
        Display a question
        """
        # ? if mnogomov_webapp.lesson.is_finished():
        # ?    return redirect(url_for('show_score'))
        question = mnogomov_webapp.lesson.current_q()
        return render_template('lesson.html',
                               question=question,
                               current_question=mnogomov_webapp.lesson.current_q_idx + 1)

    @staticmethod
    @app.route('/lesson/submit_answer')
    def submit_answer():
        answer = request.form['question_answer']
        mnogomov_webapp.lesson.check_answers(answer)
        # ? =====================================================
        # ? if mnogomov_webapp.lesson.is_finished():
        # ?    return redirect(url_for('show_score'))
        # ? =====================================================
        return redirect(url_for('display_question'))

    # ? =====================================================
    # ? @staticmethod
    # ? @app.route('/score')
    # ? def show_score():
    # ?    score = mnogomov_webapp.lesson.get_score()
    # ?    mnogomov_webapp.lesson.reset_lesson()
    # ?    return render_template('score.html', score=score)
    # ? =====================================================

    @staticmethod
    def run():
        app.run(debug=True)


if __name__ == '__main__':
    mnogomov_webapp = App()

    mnogomov_webapp.run()
