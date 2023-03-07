"""
Backend of "Mnogomov" project
"""

from flask import Flask, render_template

app = Flask(__name__, template_folder="../Mnogomov/templates")


@app.route("/")
@app.route("/home")
def home_page():
    """
    Show user the homepage
    """
    return render_template("home.html")


@app.route("/lesson/")
def lesson():
    """
    Show user the about page
    """
    return render_template('lesson.html')


if __name__ == '__main__':
    app.run(debug=True)
