"""
Backend of "Mnogomov" project
"""


from flask import Flask, render_template, request, redirect, session, url_for
import mysql.connector
from time import sleep


app = Flask(__name__, template_folder="../Mnogomov/templates")
app.secret_key = "BE_Cheporte_157E3_Legion"

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    port='3306',
    database="mnogomov"
)

cursor = db.cursor()
# Retrieve questions from db
query = "SELECT * FROM lesson"
cursor.execute(query)
questions = cursor.fetchall()
# Shut down connection
cursor.close()
db.close()

current_question = 0


@app.route('/')
def main():
    return render_template('main.html')


@app.route("/homepage")
def home():
    """
    Show user the homepage
    """
    global current_question
    current_question = 0
    return render_template("home.html")


@app.route('/about')
def about_page():
    return render_template('about.html')


@app.route('/vocabulary')
def vocabulary():
    return render_template('vocabulary.html')

@app.route('/practice')
def practice():
    return render_template('practice.html')

@app.route('/lesson')
def display_question():
    global current_question
    # Check if the user has already answered 10 questions
    if current_question >= 10:
        # Redirect the user to a new page or show a message
        return redirect("/homepage")

    # Check if we've reached the end of the questions list
    if current_question >= len(questions):
        # Reset the current_question index to 0
        current_question = 0

    # Set the current_question to 1 if it is the first question
    if current_question == 0:
        session['current_question'] = 1
    else:
        session['current_question'] = 0

    # Increment the current question index
    current_question += 1

    # Get the current question from the list of questions
    question = questions[current_question - 1]

    # Render the template with the question data
    return render_template('lesson.html', question=question, current_question=current_question)


num_of_failures = 0


@app.route('/lesson/submit_answer', methods=['GET', 'POST'])
def submit_answer():
    global current_question
    global num_of_failures
    session["last_correct_answer"] = None

    # Get the user's answer from the form data =========================================================================
    user_answer = request.form.get('question_answer')

    # Check if the user's answer is correct ============================================================================
    question = questions[current_question - 1]
    correct_answer = int(question[5])
    if user_answer == str(correct_answer):
        session["last_correct_answer"] = True
        # Increment the user's score ===================================================================================
        score = session.get('score', 0) + 1
        session['score'] = score
        # Check if the user has answered 10 questions ==================================================================
        if current_question >= 10:
            # Redirect the user to the home page with their score ======================================================
            return redirect(url_for('home', score=score))
        # Display the next question ====================================================================================
        return redirect(url_for('display_question'))
    else:
        session["last_correct_answer"] = False
        num_of_failures += 1
        session['failures'] = num_of_failures
        if num_of_failures == 3:
            session['failures'] = 0
            return redirect(url_for('home'))
        # Check if the user has answered 10 questions ==================================================================
        if current_question >= 10:
            # Redirect the user to the home page with their score ======================================================
            return redirect(url_for('home'))
        # Display the same question again ==============================================================================
        return redirect(url_for('display_question'))


if __name__ == '__main__':
    app.run(debug=True)