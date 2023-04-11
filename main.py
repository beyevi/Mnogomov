"""
Main. Runs 'Mnogomov'
"""

from __future__ import annotations
from flask import Flask, render_template, request, redirect, url_for
import lesson_quiz as lq
import db


mnogomov_webapp = Flask(__name__, template_folder="../Mnogomov/templates")
mnogomov_webapp.secret_key = "BE_Cheporte_157E3_Legion"


class App:
    """
    WebApp itself
    """

    db = db.DataBase()
    lesson = lq.LessonQuiz(db.get_questions_data())

    @mnogomov_webapp.route('/search', methods=['GET'])
    def search(self):
        """
        Used to find parameters in query
        """
        args = request.args
        result = args.get('result')
        return True if result == 'True' else False

    @staticmethod
    @mnogomov_webapp.route('/')
    def main():
        """
        Render main.html to display a welcome page.
        """
        return render_template('main.html')

    @staticmethod
    @mnogomov_webapp.route('/homepage')
    def show_homepage():
        """
        Render home.html to display a homepage.
        """
        # =====================================================
        if App().lesson.is_finished():
            return redirect(url_for('show_score'))
        # =====================================================
        App().lesson.current_q_idx = 0
        return render_template('home.html')

    @staticmethod
    @mnogomov_webapp.route('/about')
    def show_about():
        """
        Render about.html to display about page.
        """
        return render_template('about.html')

    @staticmethod
    @mnogomov_webapp.route('/vocabulary')
    def show_vocabulary():
        """
        Render vocabulary.html to display vocabulary for each lesson.
        """
        return render_template('vocabulary.html')

    @staticmethod
    @mnogomov_webapp.route('/show_score')
    def show_score():
        """
        Render a page to display user score
        """
        score = App().lesson.get_score()
        App().lesson.reset_lesson()
        return render_template('score.html', score=score)

    @staticmethod
    @mnogomov_webapp.route('/practice')
    def practice():
        """
        Render practice.html to redirect user to practice tab
        """
        return render_template('practice.html')

    @staticmethod
    @mnogomov_webapp.route('/lesson')
    def display_question():
        """
        Display a question
        """
        if App().lesson.is_finished():
            return redirect(url_for('show_score'))
        question = App().lesson.current_q()
        result = App().search()
        return render_template('lesson.html',
                               question=question,
                               id_current_question=App().lesson.current_q_idx + 1,
                               result=result)

    @staticmethod
    @mnogomov_webapp.route('/lesson/submit_answer', methods=["POST"])
    def submit_answer():
        """
        Accept user answer and send it to be checked
        """
        answer = request.form['question_answer']
        result = App().lesson.check_answers(answer)

        if App().lesson.is_finished():
            return redirect(url_for('show_score'))

        return redirect(url_for('display_question', result=result))


if __name__ == '__main__':
    mnogomov_webapp.run(debug=True)
