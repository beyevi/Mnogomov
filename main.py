"""
Backend of "Mnogomov" project
"""


from flask import Flask, render_template
import mysql.connector


app = Flask(__name__, template_folder="../Mnogomov/templates")


db = mysql.connector.connect(
    host="localhost",
    user="oigenoum",
    password="BE_Cheporte_157E3_Legion",
    database="lesson_data"
)

cursor = db.cursor()
# Retrieve questions from db
query = "SELECT * FROM question LIMIT 10"
cursor.execute(query)
questions = cursor.fetchall()
# Shut down connection
cursor.close()
db.close()

current_question = 0


@app.route("/")
def home():
    """
    Show user the homepage
    """
    return render_template("home.html")


@app.route('/lesson')
def display_question():
    global current_question

    # Check if the user has already answered 10 questions
    if current_question >= 10:
        # Redirect the user to a new page or show a message
        return render_template('home.html')

    # Check if we've reached the end of the questions list
    if current_question >= len(questions):
        # Reset the current_question index to 0
        current_question = 0

    # Get the current question from the list of questions
    question = questions[current_question]

    # Increment the current question index
    current_question += 1

    # Render the template with the question data
    return render_template('lesson.html', question=question, current_question=current_question)


if __name__ == '__main__':
    app.run(debug=True)
