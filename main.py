"""
Backend of "Mnogomov" project
"""


from flask import Flask, render_template, request, redirect, session, url_for
import mysql.connector


app = Flask(__name__, template_folder="../Mnogomov/templates")
app.secret_key = "BE_Cheporte_157E3_Legion"

db = mysql.connector.connect(
    host="localhost",
    user="oigenoum",
    password="BE_Cheporte_157E3_Legion",
    database="lesson_data"
)

cursor = db.cursor()
# Retrieve questions from db
query = "SELECT * FROM question"
cursor.execute(query)
questions = cursor.fetchall()
# Shut down connection
cursor.close()
db.close()

current_question = 0


@app.route('/')
def main():
    return render_template('main.html')


@app.route("/home")
def home():
    """
    Show user the homepage
    """
    global current_question
    current_question = 0
    return render_template("home.html")


@app.route('/lesson')
def display_question():
    global current_question
    # score = 0

    # Check if the user has already answered 10 questions
    if current_question >= 10:
        # Redirect the user to a new page or show a message
        return redirect("/home")

    # Check if we've reached the end of the questions list
    if current_question >= len(questions):
        # Reset the current_question index to 0
        current_question = 0

    # Get the current question from the list of questions
    question = questions[current_question]

    # Increment the current question index
    current_question += 1

    # if request.method == "POST":
    #     user_answer = request.form['answer']
    #     query = "SELECT correct FROM question WHERE id=%s"
    #     cursor.execute(query, (question[0],))
    #     correct_answer = cursor.fetchone()[0]
    #
    #     if int(user_answer) == correct_answer:
    #         return render_template('lesson.html', question=question, current_question=current_question, success=True)
    #     else:
    #         return render_template('lesson.html', question=question, current_question=current_question, success=False)

    # Render the template with the question data
    return render_template('lesson.html', question=question, current_question=current_question)


@app.route('/submit_answer', methods=['POST'])
def submit_answer():
    global current_question

    # Get the user's answer from the form data
    user_answer = request.form.get('answer')

    # Check if the user's answer is correct
    question = questions[current_question - 1]
    correct_answer = int(question[6])
    if user_answer == str(correct_answer):
        # Increment the user's score
        score = session.get('score', 0) + 1
        session['score'] = score
        # Check if the user has answered 10 questions
        if current_question >= 10:
            # Redirect the user to the home page with their score
            return redirect(url_for('home', score=score))
        # Display the next question
        current_question += 1
        return redirect(url_for('display_question'))
    else:
        # Check if the user has answered 10 questions
        if current_question >= 10:
            # Redirect the user to the home page with their score
            return redirect(url_for('home'))
        # Display the same question again
        return redirect(url_for('display_question'))


if __name__ == '__main__':
    app.run(debug=True)
