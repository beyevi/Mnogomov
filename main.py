from flask import Flask, render_template
import os

template_dir = os.path.abspath('/home/oigenoum/PycharmProjects/Mnogomov/frontend/templates')
app = Flask(__name__, template_folder=template_dir)

@app.route("/")
@app.route("/home")
def home_page():
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)