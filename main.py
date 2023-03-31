"""
Main. Runs 'Mnogomov'
"""

from flask import Flask, render_template, request, redirect, url_for
import lesson_quiz as lq
import db


app = Flask(__name__, template_folder="../Mnogomov/templates")
app.secret_key = "BE_Cheporte_157E3_Legion"


class App:
    """
    WebApp itself
    """

    def __init__(self):
        self.db = db.DataBase()
        self.lesson = lq.LessonQuiz(self.db.get_questions_data())

    @app.route('/search', methods=['GET'])
    def search(self):
        """
        Used to find parameters in query
        """
        args = request.args
        result = args.get('result')
        return True if result == 'True' else False

    @staticmethod
    @app.route('/')
    def main():
        """
        Render main.html to display a welcome page.
        """
        return render_template('main.html')

    @staticmethod
    @app.route('/homepage')
    def show_homepage():
        """
        Render home.html to display a homepage.
        """
        # =====================================================
        if mnogomov_webapp.lesson.is_finished():
            return redirect(url_for('show_score'))
        # =====================================================
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
    @app.route('/show_score')
    def show_score():
        """
        Render a page to display user score
        """
        score = mnogomov_webapp.lesson.get_score()
        mnogomov_webapp.lesson.reset_lesson()
        return render_template('score.html', score=score)

    @staticmethod
    @app.route('/practice')
    def practice():
        """
        Render practice.html to redirect user to practice tab
        """
        return render_template('practice.html')

    @staticmethod
    @app.route('/lesson')
    def display_question():
        """
        Display a question
        """
        if mnogomov_webapp.lesson.is_finished():
            return redirect(url_for('show_score'))
        question = mnogomov_webapp.lesson.current_q()
        result = mnogomov_webapp.search()
        print(result)
        return render_template('lesson.html',
                               question=question,
                               id_current_question=mnogomov_webapp.lesson.current_q_idx + 1,
                               result=result)

    @staticmethod
    @app.route('/lesson/submit_answer', methods=["POST"])
    def submit_answer():
        """
        Accept user answer and send it to be checked
        """
        answer = request.form['question_answer']
        result = mnogomov_webapp.lesson.check_answers(answer)

        if mnogomov_webapp.lesson.is_finished():
            return redirect(url_for('show_score'))

        return redirect(url_for('display_question', result=result))

    @staticmethod
    def run():
        """
        Run 'Mnogomov'
        """
        app.run(debug=True)


if __name__ == '__main__':
    mnogomov_webapp = App()

    mnogomov_webapp.run()
