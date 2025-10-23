from flask import Flask, render_template
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
template_dir = os.path.join(os.path.dirname(current_dir), 'ui')
static_dir = os.path.join(os.path.dirname(current_dir), 'ui')

app = Flask(__name__, template_folder=template_dir, static_folder=static_dir, static_url_path='/static')
app.secret_key = os.urandom(16)

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login')
def login():
    return render_template('login.html')

if __name__ == '__main__':
    app.run(debug=True)